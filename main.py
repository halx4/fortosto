from __future__ import annotations

import csv

import psycopg2

from commons.CastDataType import CastDataType
from commons.TableNormalizer import TableNormalizer
from commons.dao import DAO
from properties import Properties
from initializer import initialize
from commons.loggingUtils import getRootLogger

log = getRootLogger()


def main():
    initialize()

    dao = DAO(Properties.developmentMode)

    (headers, dataRows) = getCsvDataFromLocalFile(Properties.filename)

    (newHeaders, newRecords) = TableNormalizer.normalizeHeadersForTable(headers, dataRows)

    print(newHeaders)

    try:
        dao.createVarCharTable(Properties.schema, Properties.table, newHeaders)
        dao.saveRecordsToDb(Properties.schema, Properties.table, newRecords)
    except psycopg2.DatabaseError as e:
        log.error("Db error: " + str(e))
        exit(1)

    ## casting attempt of columns (except the id column)
    tryCastingHeaders(dao, newHeaders)


def tryCastingHeaders(dao: DAO, columns: list):
    castResults = dict()
    for header in columns:
        castResult = tryCastingColumn(dao, header)
        if castResult is not None:
            castResults[header] = str(castResult.name)

    log.info('conversions made:')
    log.info(castResults)
    return castResults


def tryCastingColumn(dao: DAO, header: str) -> CastDataType:
    log.debug(f"attempting cast column {header}")
    ### integer
    try:
        log.debug("> casting to  Integer...")
        dao.castColumnToInteger(Properties.schema, Properties.table, header)
        log.debug("> casting to  Integer succeeded")
        return CastDataType.Integer
    except Exception as e:
        log.debug("> casting to  Integer failed")
        print(e)

    ### double
    try:
        log.debug("> casting to  Float...")
        dao.castColumnToFloat(Properties.schema, Properties.table, header)
        log.debug("> casting to  Float succeeded")
        return CastDataType.Double
    except Exception as e:
        log.debug("> casting to  Float failed")
        print(e)

    ### date
    # TODO

    return None


def getCsvDataFromLocalFile(filePath: str) -> tuple:
    # get the headers as list
    with open(filePath, mode='r', newline='', encoding=Properties.fileEncoding) as csv_file:
        csvReader = csv.reader(csv_file, delimiter=Properties.delimiter, quotechar='"')
        headers = next(csvReader)

    with open(filePath, mode='r', newline='', encoding=Properties.fileEncoding) as csv_file:
        csvReader = csv.DictReader(csv_file, delimiter=Properties.delimiter, quotechar='"')

        dataRows = list()
        for row in csvReader:
            dataRows.append(row)

    # print(headers)
    # for rec in dataRows:
    #     print(rec)
    return (headers, dataRows)


if __name__ == '__main__':
    main()
