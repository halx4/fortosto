from psycopg2._psycopg import AsIs

from commons.PostgresCastException import PostgresCastException
from commons.PostgresException import PostgresException
from commons.UnableToSaveException import UnableToSaveException
from commons.sqlTemplates import getCreateTableQuery, getCastColumnToIntegerQuery, getCastColumnToFloatQuery, \
    getDropTableQuery
from properties import Properties
import psycopg2
import psycopg2.extras
import psycopg2.errorcodes

from commons.loggingUtils import getRootLogger

log = getRootLogger()


class DAO(object):
    def __init__(self, developmentMode=False, conn=None):

        self.developmentMode = developmentMode

        if conn is not None:
            self.conn = conn
            self.connected = False
            return

        # else
        self.connected = False
        try:
            self.conn = psycopg2.connect(
                dbname=Properties.dbname,
                user=Properties.user,
                password=Properties.password,
                host=Properties.host,
                port=Properties.port
            )
            self.connected = True

        except:
            log.error("Could not connect to the database")

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
        sql = getCreateTableQuery(schema, tableName, columns,idColumn)
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
            columns = ','.join([t[0] for t in l])

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
            columns = ','.join([t[0] for t in l])

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
