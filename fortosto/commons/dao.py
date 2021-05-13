from typing import List

from psycopg2._psycopg import AsIs

from .PostgresException import PostgresException
from .UnableToSaveException import UnableToSaveException
from .sqlTemplates import getCreateTableQuery, getCastColumnToIntegerQuery, getCastColumnToFloatQuery, \
    getDropTableQuery, getTruncateTableQuery, getCastColumnToDateQuery

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

    def getColumnsInfoOfTable(self, schema: str, table: str) -> List[dict]:
        cur = self.conn.cursor()
        self.execute(cur, f"""SELECT 
	column_name,ordinal_position,column_default,is_nullable,data_type,is_identity
 FROM information_schema.columns 
 WHERE table_schema = '{schema}' 
 AND table_name   = '{table}';""")
        self.conn.commit()
        rawResult = cur.fetchall()
        result = [
            {'column_name': x[0],
             'ordinal_position': x[1],
             'column_default': x[2],
             'is_nullable': True if x[3] == 'YES' else False,
             'data_type': x[4],
             'is_identity': True if x[5] == 'YES' else False
             } for x in rawResult]
        return result

    #################################################################
    def schemaExists(self, schema: str):
        cur = self.conn.cursor()
        self.execute(cur, f"SELECT EXISTS(SELECT FROM information_schema.schemata WHERE schema_name = '{schema}');")
        self.conn.commit()
        (result,) = cur.fetchone()
        return result

    #################################################################

    def tableExists(self, schema: str, table: str):
        cur = self.conn.cursor()
        self.execute(cur,
                     f"SELECT EXISTS(SELECT FROM information_schema.tables WHERE table_schema = '{schema}' AND table_name = '{table}');")
        self.conn.commit()
        (result,) = cur.fetchone()
        return result

    #################################################################

    def castColumnToFloat(self, schema: str, table: str, column: str):
        sql = getCastColumnToFloatQuery(schema, table, column)
        cur = self.conn.cursor()

        self.execute(cur, sql)
        self.conn.commit()

    #################################################################

    def castColumnToInteger(self, schema: str, table: str, column: str):
        sql = getCastColumnToIntegerQuery(schema, table, column)
        cur = self.conn.cursor()

        self.execute(cur, sql)
        self.conn.commit()

    #################################################################

    def castColumnToDate(self, schema: str, table: str, column: str, format: str):
        sql = getCastColumnToDateQuery(schema, table, column, format)
        cur = self.conn.cursor()

        self.execute(cur, sql)
        self.conn.commit()

    #################################################################

    def createVarCharTable(self, schema: str, table: str, columns: List[str], idColumn: str = None):
        sql = getCreateTableQuery(schema, table, columns, idColumn)
        cur = self.conn.cursor()
        self.execute(cur, sql)
        self.conn.commit()

    #################################################################

    def dropTable(self, schema: str, table: str):
        sql = getDropTableQuery(schema, table, ifExists=True)
        cur = self.conn.cursor()
        self.execute(cur, sql)
        self.conn.commit()

    #################################################################

    def truncateTable(self, schema: str, table: str, restartIdentity: bool = False, cascade: bool = False):
        sql = getTruncateTableQuery(schema, table, restartIdentity, cascade)
        cur = self.conn.cursor()
        self.execute(cur, sql)
        self.conn.commit()

    #################################################################

    def getRecordCountOfTable(self, schema: str, table: str):
        cur = self.conn.cursor()
        self.execute(cur, f'SELECT count(*) FROM "{schema}"."{table}";')
        self.conn.commit()
        rawResult = cur.fetchone()
        result = rawResult[0]
        return result

    #################################################################

    def saveRecordsToDb(self, schema: str, table: str, recordsAsList: List[dict]):
        return self.insertValues(schema, table, recordsAsList)

    #################################################################
    #################################################################

    # PRIVATE METHODS
    def insertValues(self, schema, table, records: List[dict]):
        """raises UnableToSaveException
        """

        if (not self.connected):
            raise UnableToSaveException("Client is not connected to the database")
        elif (not records):  # list is empty
            return
        else:
            # columns
            record0 = records[0]

            l = [(c, v) for c, v in record0.items()]
            columns = ','.join([f'"{t[0]}"' for t in l])

            recordsAsTuplesList = list()
            # values for each record
            for record in records:
                l = [(c, v) for c, v in record.items()]
                values = tuple([t[1] for t in l])
                recordsAsTuplesList.append(values)

            insert = f'insert into "{schema}"."{table}" ({columns}) values %s'

            cur = self.conn.cursor()

            self.executeValues(cur, insert, recordsAsTuplesList)

            self.conn.commit()

    def insertValuesOnConflictUpdate(self, schema: str, table: str, recordsAsList):
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
            insert = f'insert into "{schema}"."{table}" ({columns}) values %s on conflict (id) do update set {updateQueryPart}'

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
