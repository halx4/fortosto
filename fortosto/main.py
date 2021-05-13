from __future__ import annotations

import psycopg2

from .initializer import initialize
from .fortosto import Fortosto
from .commons.loggingUtils import getRootLogger

log = getRootLogger()


class Standalone:

    @staticmethod
    def run():
        initResult = initialize()

        conn = psycopg2.connect(
            dbname=initResult.dbname,
            user=initResult.user,
            password=initResult.password,
            host=initResult.host,
            port=initResult.port
        )
        log.info("DB connection established successfully")

        core = Fortosto(
            conn=conn,
            schema=initResult.schema,
            delimiter=initResult.delimiter,
            tableNamePrefix=initResult.tableNamePrefix,
            primaryKey=initResult.primaryKey,
            filenamePattern=initResult.filenamePattern,
            dropTableIfExists=initResult.dropTableIfExists,
            castNumbers=initResult.castNumbers,
            target=initResult.target,
            table=initResult.table,
            appendMode=initResult.appendMode
        )

        return core.fortosto()


if __name__ == '__main__':
    Standalone.run()
