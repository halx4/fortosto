from __future__ import annotations
from itertools import islice
import csv
import json
import traceback

import psycopg2
from collections import namedtuple

from commons.CastDataType import CastDataType
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

dao = None

TargetInfo = namedtuple('TargetInfo', ['filePath', 'table'])


def main():
    initialize()

    # initialize db connection
    global dao
    dao = DAO(Properties.developmentMode)
    log.info("DB connection established successfully")

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
    processTargets(targetsList)


def processTargets(targets: list):
    '''

    :param targets: list of namedtuples
    :return:
    '''
    failedTargets = list()
    for target in targets:
        try:
            log.info(f"Starting processing file {target}")
            processTarget(target)
            log.info(f"processing file {target} completed successfully")
        except Exception as e:
            stacktrace = traceback.format_exc()
            log.error(stacktrace)
            failedTargets.append((target[0], target[1], stacktrace))
    for entry in failedTargets:
        log.warning(f"failed: {entry}")


def processTarget(target: namedtuple):
    global dao

    fileType = FileType.csv
    # determine if the file is csv or jsonl
    if isJsonlTarget(target.filePath):
        log.info("jsonl file")
        fileType = FileType.jsonl
    else:
        log.info("csv file")

    headers = getHeadersFromLocalFile(fileType, target.filePath)
    log.debug(f"headers: {headers}")

    newHeaders = TableNormalizer.normalizeHeaders(headers)
    log.debug(f"normalised headers: {newHeaders}")

    if Properties.dropTableIfExists:
        log.debug(f"dropping table: {target.table}")
        dao.dropTable(Properties.schema, target.table)

    dao.createVarCharTable(Properties.schema, target.table, newHeaders, Properties.primaryKey)

    importToDbTable(target, headers, newHeaders, fileType)

    if (Properties.castNumbers):
        ## casting attempt of columns (except the id column)
        tryCastingHeaders(dao, newHeaders)


def importToDbTable(target: namedtuple, headers, newHeaders, fileType: FileType):
    if (fileType == FileType.csv):
        return importCsvToDbTable(target, headers, newHeaders)
    elif fileType == FileType.jsonl:
        return importJsonlToDbTable(target, headers, newHeaders)
    else:
        raise UnexpectedEnumValueException(f"got value: {fileType}")


def importJsonlToDbTable(target: namedtuple, headers, newHeaders):
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
                dao.saveRecordsToDb(Properties.schema, target.table, normalizedRecords)
            except psycopg2.DatabaseError as e:
                log.error("Db error: " + str(e))
                exit(1)


def importCsvToDbTable(target: namedtuple, headers, newHeaders):
    with open(target.filePath, mode='r', newline='', encoding=Properties.fileEncoding) as csv_file:
        csvReader = csv.DictReader(csv_file, delimiter=Properties.delimiter, quotechar='"')

        hasMore = True
        batchNo = 0
        while hasMore:
            batchNo += 1
            log.info(f"batchNo: {batchNo}, record: {batchNo * batchSize}")
            (batchDataRows, hasMore) = getNextBatch(csvReader)
            normalizedRecords = TableNormalizer.normalizeRecords(headers, newHeaders, batchDataRows)
            try:
                dao.saveRecordsToDb(Properties.schema, target.table, normalizedRecords)
            except psycopg2.DatabaseError as e:
                log.error("Db error: " + str(e))
                exit(1)


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


def getHeadersFromLocalFile(fileType: FileType, filePath: str):
    if (fileType == FileType.csv):
        return getCsvHeadersFromLocalFile(filePath)
    elif fileType == FileType.jsonl:
        return getJsonlHeadersFromLocalFile(filePath)
    else:
        raise UnexpectedEnumValueException(f"got value: {fileType}")


def getJsonlHeadersFromLocalFile(filePath: str) -> list:
    with open(filePath, mode='r', newline='', encoding=Properties.fileEncoding) as file:
        firstLine = file.readline()
        firstLineAsDict = json.loads(firstLine)

        return list(firstLineAsDict)


def getCsvHeadersFromLocalFile(filePath: str) -> list:
    # get the headers as list
    with open(filePath, mode='r', newline='', encoding=Properties.fileEncoding) as csv_file:
        csvReader = csv.reader(csv_file, delimiter=Properties.delimiter, quotechar='"')
        headers = next(csvReader)
    return headers


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


if __name__ == '__main__':
    main()
