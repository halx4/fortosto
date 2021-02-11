from psycopg2._psycopg import AsIs

from commons.UnableToSaveException import UnableToSaveException
from commons.sqlTemplates import getCreateTableQuery
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

    def createVarCharTable(self, schema: str, tableName: str, columns: list):
        sql = getCreateTableQuery(schema, tableName, columns)
        cur = self.conn.cursor()
        self.execute(cur, sql)
        self.conn.commit()

    #################################################################
    # UPDATED
    def saveRecordsToDb(self, schema: str, table: str, recordsAsList: list):
        return self.insertValues(schema, table, recordsAsList)

    #################################################################

    #################################################################

    # PRIVATE METHODS
    def insertValues(self,schema, tableName, recordsAsList):
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

            insert = f'insert into {schema}.{tableName} ({columns}) values %s'

            cur = self.conn.cursor()

            self.executeValues(cur, insert, recordsAsTuplesList)

            self.conn.commit()

    def insertValuesOnConflictUpdate(self, tableName, recordsAsList):
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
            insert = f'insert into {tableName} ({columns}) values %s on conflict (id) do update set {updateQueryPart}'

            cur = self.conn.cursor()
            self.executeValues(cur, insert, recordsAsTuplesList)
            self.conn.commit()

    def execute(self, cur, query, variables=None):
        if (self.developmentMode):
            log.warn("dry-run (dev mode) query: " + str(query))
            return None
        else:
            return cur.execute(query, variables)

    def executeValues(self, cur, query, argslist, template=None, page_size=100, fetch=False):
        if (self.developmentMode):
            log.warn("dry-run (dev mode) query: " + str(query))
            return None
        return psycopg2.extras.execute_values(cur, query, argslist, template, page_size, fetch)
