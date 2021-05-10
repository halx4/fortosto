from __future__ import annotations
from itertools import islice
import csv
import json
import traceback

import psycopg2
from collections import namedtuple

import glob

from commons.FileType import FileType
from commons.TableNormalizer import TableNormalizer
from commons.UnexpectedEnumValueException import UnexpectedEnumValueException
from commons.Utils import isJsonlTarget
from commons.castingUtils import tryCastingHeaders
from commons.dao import DAO
from commons.stringsNormalizer import StringsNormalizer
from properties import Properties
from initializer import initialize
from commons.loggingUtils import getRootLogger
import os.path
from os import path

log = getRootLogger()

batchSize = Properties.batchSize


TargetInfo = namedtuple('TargetInfo', ['filePath', 'table'])


class Fortosto:
    conn = None
    dao = None

    @staticmethod
    def fortosto(conn):
        initialize()


        # initialize db connection
        Fortosto.dao = DAO.fromConnection(conn, developmentMode=Properties.developmentMode)

        target = Properties.target
        if path.exists(target):
            log.debug('target exists')
        else:
            log.error(f'target not found( {target} )')
            exit(1)

        if os.path.isdir(target):
            log.debug("It is a directory")

            # add a trailing dash to the folder path if it doesnt have one
            target = target + "/" if not target.endswith("/") else target

            filenamePattern = f'{target}{Properties.filenamePattern}'
            log.info(f"filenamePattern= {filenamePattern}")
            targetsFilenames = sorted(glob.glob(filenamePattern, recursive=True))
            # consider filtering out dirs
            targetsList = [TargetInfo(filePath=target,
                                      table=Properties.tableNamePrefix + StringsNormalizer.filenameToNormalisedTableName(
                                          target)) for target in targetsFilenames]
        else:
            log.debug("Not a dir")
            targetsList = [TargetInfo(filePath=target, table=Properties.tableNamePrefix + Properties.table)]

        log.info(f"targetsList={targetsList}")
        Fortosto.processTargets(targetsList)

    @staticmethod
    def processTargets(targets: list):
        '''

        :param targets: list of namedtuples
        :return:
        '''
        failedTargets = list()
        for target in targets:
            try:
                log.info(f"Starting processing file {target}")
                Fortosto.processTarget(target)
                log.info(f"processing file {target} completed successfully")
            except Exception as e:
                stacktrace = traceback.format_exc()
                log.error(stacktrace)
                failedTargets.append((target[0], target[1], stacktrace))
        for entry in failedTargets:
            log.warning(f"failed: {entry}")

    @staticmethod
    def processTarget(target: TargetInfo):

        fileType = FileType.csv
        # determine if the file is csv or jsonl
        if isJsonlTarget(target.filePath, Properties.jsonlFileExtensions):
            log.info("jsonl file")
            fileType = FileType.jsonl
        else:
            log.info("csv file")

        headers = Fortosto.getHeadersFromLocalFile(fileType, target.filePath)
        log.debug(f"headers: {headers}")

        newHeaders = TableNormalizer.normalizeHeaders(headers)
        log.debug(f"normalised headers: {newHeaders}")

        if Properties.dropTableIfExists:
            log.debug(f"dropping table: {target.table}")
            Fortosto.dao.dropTable(Properties.schema, target.table)

        Fortosto.dao.createVarCharTable(Properties.schema, target.table, newHeaders, Properties.primaryKey)

        Fortosto.importToDbTable(target, headers, newHeaders, fileType)

        if (Properties.castNumbers):
            ## casting attempt of columns (except the id column)
            tryCastingHeaders(Fortosto.dao, Properties.schema, Properties.table, newHeaders)

    @staticmethod
    def importToDbTable(target: TargetInfo, headers, newHeaders, fileType: FileType):
        if (fileType == FileType.csv):
            return Fortosto.importCsvToDbTable(target, headers, newHeaders)
        elif fileType == FileType.jsonl:
            return Fortosto.importJsonlToDbTable(target, headers, newHeaders)
        else:
            raise UnexpectedEnumValueException(f"got value: {fileType}")

    @staticmethod
    def importJsonlToDbTable(target: TargetInfo, headers, newHeaders):
        with open(target.filePath, mode='r', newline='', encoding=Properties.fileEncoding) as file:

            batchNo = 0

            while True:
                batchDataRowsAsListOfStrings = list(islice(file, batchSize))
                records = [json.loads(x) for x in batchDataRowsAsListOfStrings]
                if not batchDataRowsAsListOfStrings:  # true when batchDataRows is empty list
                    break
                # process the batch
                batchNo += 1
                log.info(f"batchNo: {batchNo}, record: {batchNo * batchSize}")

                normalizedRecords = TableNormalizer.normalizeRecords(headers, newHeaders, records)
                try:
                    Fortosto.dao.saveRecordsToDb(Properties.schema, target.table, normalizedRecords)
                except psycopg2.DatabaseError as e:
                    log.error("Db error: " + str(e))
                    exit(1)

    @staticmethod
    def importCsvToDbTable(target: TargetInfo, headers, newHeaders):
        with open(target.filePath, mode='r', newline='', encoding=Properties.fileEncoding) as csv_file:
            csvReader = csv.DictReader(csv_file, delimiter=Properties.delimiter, quotechar='"')

            hasMore = True
            batchNo = 0
            while hasMore:
                batchNo += 1
                log.info(f"batchNo: {batchNo}, record: {batchNo * batchSize}")
                (batchDataRows, hasMore) = Fortosto.getNextBatch(csvReader)
                normalizedRecords = TableNormalizer.normalizeRecords(headers, newHeaders, batchDataRows)
                try:
                    Fortosto.dao.saveRecordsToDb(Properties.schema, target.table, normalizedRecords)
                except psycopg2.DatabaseError as e:
                    log.error("Db error: " + str(e))
                    exit(1)

    @staticmethod
    def getNextBatch(csvReader) -> tuple:
        batch = list()

        try:
            i = batchSize
            while i > 0:
                row = next(csvReader)
                batch.append(row)
                i -= 1
        except StopIteration:
            log.info("reached end of iterator")
            return (batch, False)

        return (batch, True)

    @staticmethod
    def getHeadersFromLocalFile(fileType: FileType, filePath: str):
        if (fileType == FileType.csv):
            return Fortosto.getCsvHeadersFromLocalFile(filePath)
        elif fileType == FileType.jsonl:
            return Fortosto.getJsonlHeadersFromLocalFile(filePath)
        else:
            raise UnexpectedEnumValueException(f"got value: {fileType}")

    @staticmethod
    def getJsonlHeadersFromLocalFile(filePath: str) -> list:
        with open(filePath, mode='r', newline='', encoding=Properties.fileEncoding) as file:
            firstLine = file.readline()
            firstLineAsDict = json.loads(firstLine)

            return list(firstLineAsDict)

    @staticmethod
    def getCsvHeadersFromLocalFile(filePath: str) -> list:
        # get the headers as list
        with open(filePath, mode='r', newline='', encoding=Properties.fileEncoding) as csv_file:
            csvReader = csv.reader(csv_file, delimiter=Properties.delimiter, quotechar='"')
            headers = next(csvReader)
        return headers

    @staticmethod
    def getCsvDataFromLocalFile(filePath: str) -> list:
        with open(filePath, mode='r', newline='', encoding=Properties.fileEncoding) as csv_file:
            csvReader = csv.DictReader(csv_file, delimiter=Properties.delimiter, quotechar='"')

            dataRows = list()
            for row in csvReader:
                dataRows.append(row)

        # print(headers)
        # for rec in dataRows:
        #     print(rec)
        return dataRows
