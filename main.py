from __future__ import annotations

import csv

import psycopg2

from commons.CastDataType import CastDataType
from commons.TableNormalizer import TableNormalizer
from commons.castingUtils import tryCastingHeaders
from commons.dao import DAO
from properties import Properties
from initializer import initialize
from commons.loggingUtils import getRootLogger

log = getRootLogger()

batchSize = Properties.batchSize


def main():
    initialize()

    dao = DAO(Properties.developmentMode)

    headers = getCsvHeadersFromLocalFile(Properties.filename)
    log.debug(f"headers: {headers}")

    newHeaders = TableNormalizer.normalizeHeaders(headers)
    log.debug(f"normalised headers: {newHeaders}")



    try:
        if Properties.dropTableIfExists:
            log.debug(f"dropping table: {Properties.table}")
            dao.dropTable(Properties.schema, Properties.table)

        dao.createVarCharTable(Properties.schema, Properties.table, newHeaders)
    except psycopg2.DatabaseError as e:
        log.error("Db error: " + str(e))
        exit(1)

    with open(Properties.filename, mode='r', newline='', encoding=Properties.fileEncoding) as csv_file:
        csvReader = csv.DictReader(csv_file, delimiter=Properties.delimiter, quotechar='"')

        hasMore = True
        batchNo = 0
        while hasMore:
            batchNo += 1
            log.info(f"batchNo: {batchNo}, record: {batchNo * batchSize}")
            (batchDataRows, hasMore) = getNextBatch(csvReader)
            normalizedRecords = TableNormalizer.normalizeRecords(headers, newHeaders, batchDataRows)
            try:
                dao.saveRecordsToDb(Properties.schema, Properties.table, normalizedRecords)
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
