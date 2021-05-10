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
    return Fortosto.fortosto(conn)




if __name__ == '__main__':
    main()
