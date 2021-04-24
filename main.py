from __future__ import annotations

import csv

import psycopg2
from collections import namedtuple

from commons.CastDataType import CastDataType
import glob

from commons.TableNormalizer import TableNormalizer
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

TargetInfo=namedtuple('TargetInfo',['filePath','table'])

def main():
    initialize()

    global dao
    dao = DAO(Properties.developmentMode)

    target = './testData/bulk/'
    if path.exists(target):
        log.debug('target exists')
    else:
        log.debug('target not found')
        exit(1)

    if os.path.isdir(target):
        log.debug("It is a directory")
        filenamePattern = f'{target}{Properties.filenamePattern}'
        log.info(f"filenamePattern= {filenamePattern}")
        targetsFilenames = sorted(glob.glob(filenamePattern, recursive=True))
        # consider filtering out dirs
        targetsList = [TargetInfo(filePath=target, table=StringsNormalizer.filenameToNormalisedTableName(target)) for target in targetsFilenames]
    else:
        log.debug("It is Not a dir")
        targetsList = TargetInfo(filePath=target,  table=Properties.table)

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
            log.error(e)
            failedTargets.append((target[0], target[1], e))
    log.warning(f"failed targets: {failedTargets}")


def processTarget(target: namedtuple):
    global dao
    headers = getCsvHeadersFromLocalFile(target.filePath)
    log.debug(f"headers: {headers}")

    newHeaders = TableNormalizer.normalizeHeaders(headers)
    log.debug(f"normalised headers: {newHeaders}")

    if Properties.dropTableIfExists:
        log.debug(f"dropping table: {target.table}")
        dao.dropTable(Properties.schema, target.table)

    dao.createVarCharTable(Properties.schema, target.table, newHeaders)

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

    if(Properties.castNumbers):
        ## casting attempt of columns (except the id column)
        tryCastingHeaders(dao, newHeaders)


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
