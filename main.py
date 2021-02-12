import csv

import psycopg2

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
