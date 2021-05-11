from psycopg2._psycopg import AsIs

from .PostgresException import PostgresException
from .UnableToSaveException import UnableToSaveException
from .sqlTemplates import getCreateTableQuery, getCastColumnToIntegerQuery, getCastColumnToFloatQuery, \
    getDropTableQuery

import psycopg2
import psycopg2.extras
import psycopg2.errorcodes

from .loggingUtils import getRootLogger

log = getRootLogger()


class DAO(object):

    @staticmethod
    def fromConnection(conn, developmentMode=False):
        return DAO(developmentMode, conn)

    @staticmethod
    def fromConnectionDetails(
            dbname,
            user,
            password,
            host,
            port,
            developmentMode=False):

        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            return DAO(developmentMode, conn)

        except Exception as e:
            raise PostgresException("Could not establish connection to the database", e)

    def __init__(self, developmentMode=False, conn=None):

        if conn is not None:
            self.developmentMode = developmentMode
            self.conn = conn
            self.connected = True
            return
        else:
            raise PostgresException("conn object cannot be None")

    #################################################################

    def getTablesOfSchema(self, schema: str):
        cur = self.conn.cursor()
        self.execute(cur, f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}'")
        self.conn.commit()
        rawResult = cur.fetchall()
        result = [x[0] for x in rawResult]
        return result

    #################################################################

    def schemaExists(self, schema: str):
        cur = self.conn.cursor()
        self.execute(cur, f"SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = '{schema}');")
        self.conn.commit()
        (result,) = cur.fetchone()
        return result

    #################################################################

    def castColumnToFloat(self, schema: str, tableName: str, column: str):
        sql = getCastColumnToFloatQuery(schema, tableName, column)
        cur = self.conn.cursor()

        self.execute(cur, sql)
        self.conn.commit()

    #################################################################

    def castColumnToInteger(self, schema: str, tableName: str, column: str):
        sql = getCastColumnToIntegerQuery(schema, tableName, column)
        cur = self.conn.cursor()

        self.execute(cur, sql)
        self.conn.commit()

    #################################################################

    def createVarCharTable(self, schema: str, tableName: str, columns: list, idColumn=None):
        sql = getCreateTableQuery(schema, tableName, columns, idColumn)
        cur = self.conn.cursor()
        self.execute(cur, sql)
        self.conn.commit()

    #################################################################

    def dropTable(self, schema: str, tableName: str):
        sql = getDropTableQuery(schema, tableName, ifExists=True)
        cur = self.conn.cursor()
        self.execute(cur, sql)
        self.conn.commit()

    #################################################################

    def saveRecordsToDb(self, schema: str, table: str, recordsAsList: list):
        return self.insertValues(schema, table, recordsAsList)

    #################################################################
    #################################################################

    # PRIVATE METHODS
    def insertValues(self, schema, tableName, recordsAsList):
        """raises UnableToSaveException
        """

        if (not self.connected):
            raise UnableToSaveException("Client is not connected to the database")
        elif (not recordsAsList):  # list is empty
            return
        else:
            # columns
            record0 = recordsAsList[0]

            l = [(c, v) for c, v in record0.items()]
            columns = ','.join([f'"{t[0]}"' for t in l])

            recordsAsTuplesList = list()
            # values for each record
            for record in recordsAsList:
                l = [(c, v) for c, v in record.items()]
                values = tuple([t[1] for t in l])
                recordsAsTuplesList.append(values)

            insert = f'insert into "{schema}"."{tableName}" ({columns}) values %s'

            cur = self.conn.cursor()

            self.executeValues(cur, insert, recordsAsTuplesList)

            self.conn.commit()

    def insertValuesOnConflictUpdate(self, schema: str, tableName: str, recordsAsList):
        """raises UnableToSaveException
        """

        if (not self.connected):
            raise UnableToSaveException("Client is not connected to the database")
        elif (not recordsAsList):  # list is empty
            return
        else:
            # columns
            record0 = recordsAsList[0]

            l = [(c, v) for c, v in record0.items()]
            columns = ','.join([f'"{t[0]}"' for t in l])

            recordsAsTuplesList = list()
            # values for each record
            for record in recordsAsList:
                l = [(c, v) for c, v in record.items()]
                values = tuple([t[1] for t in l])
                recordsAsTuplesList.append(values)

            updateQueryPart = ','.join([t[0] + "=excluded." + t[0] for t in l])
            insert = f'insert into "{schema}"."{tableName}" ({columns}) values %s on conflict (id) do update set {updateQueryPart}'

            cur = self.conn.cursor()
            self.executeValues(cur, insert, recordsAsTuplesList)
            self.conn.commit()

    def execute(self, cur, query, variables=None):
        if (self.developmentMode):
            log.warn("dry-run (dev mode) query: " + str(query))
            return None
        else:
            try:
                return cur.execute(query, variables)
            except Exception as e:
                self.conn.rollback()
                raise PostgresException() from e

    def executeValues(self, cur, query, argslist, template=None, page_size=100, fetch=False):
        if (self.developmentMode):
            log.warn("dry-run (dev mode) query: " + str(query))
            return None
        try:
            return psycopg2.extras.execute_values(cur, query, argslist, template, page_size, fetch)
        except Exception as e:
            self.conn.rollback()
            raise PostgresException() from e
