from __future__ import annotations

import psycopg2

from properties import Properties
from initializer import initialize
from fortosto import Fortosto
from commons.loggingUtils import getRootLogger

log = getRootLogger()


def main():
    initialize()

    conn = psycopg2.connect(
        dbname=Properties.dbname,
        user=Properties.user,
        password=Properties.password,
        host=Properties.host,
        port=Properties.port
    )
    log.info("DB connection established successfully")

    core = Fortosto(
        conn=conn,
        schema=Properties.schema,
        delimiter=Properties.delimiter,
        tableNamePrefix=Properties.tableNamePrefix,
        primaryKey=Properties.primaryKey,
        filenamePattern=Properties.filenamePattern,
        dropTableIfExists=Properties.dropTableIfExists,
        castNumbers=Properties.castNumbers,
        target=Properties.target,
        table=Properties.table
    )

    return core.fortosto()


if __name__ == '__main__':
    main()
