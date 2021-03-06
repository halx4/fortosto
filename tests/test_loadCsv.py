import unittest
from fortosto.commons.dao import DAO
from tests.TestConfigurationProvider import TestConfigurationProvider
import psycopg2
from fortosto.fortosto import Fortosto


class TestLoadCsv(unittest.TestCase):

    def setUp(self):
        conn = psycopg2.connect(
            dbname=TestConfigurationProvider.dbname,
            user=TestConfigurationProvider.user,
            password=TestConfigurationProvider.password,
            host=TestConfigurationProvider.host,
            port=TestConfigurationProvider.port
        )
        self.dao = DAO.fromConnection(conn, False)

        self.fortostoConn = psycopg2.connect(
            dbname=TestConfigurationProvider.dbname,
            user=TestConfigurationProvider.user,
            password=TestConfigurationProvider.password,
            host=TestConfigurationProvider.host,
            port=TestConfigurationProvider.port
        )

    def test_load(self):
        table = "test_load_csv"
        
        print(f"dropping test table: {table}")
        self.dao.dropTable(schema=TestConfigurationProvider.schema, table=table)
        exists = self.dao.tableExists(schema=TestConfigurationProvider.schema, table=table)
        self.assertFalse(exists)

        engine = Fortosto(
            conn=self.fortostoConn,
            schema=TestConfigurationProvider.schema,
            delimiter=',',
            tableNamePrefix='',
            primaryKey='',
            filenamePattern='',
            dropTableIfExists=False,
            castNumbers=True,
            target='./testData/csv-2MB-1.csv',
            table=table,
            appendMode=False
        )
        engine.fortosto()

        count = self.dao.getRecordCountOfTable(schema=TestConfigurationProvider.schema, table=table)
        self.assertEqual(count, 33321)

        columnsInfo = self.dao.getColumnsInfoOfTable(schema=TestConfigurationProvider.schema, table=table)
        firstdoseInfo = next(item for item in columnsInfo if item["column_name"] == "firstdose")
        self.assertEqual(firstdoseInfo['data_type'], 'integer')

        denominatorInfo = next(item for item in columnsInfo if item["column_name"] == "denominator")
        self.assertEqual(denominatorInfo['data_type'], 'integer')

    def test_load_with_id(self):
        table = "test_load_csv_with_id"

        print(f"dropping test table: {table}")
        self.dao.dropTable(schema=TestConfigurationProvider.schema, table=table)

        engine = Fortosto(
            conn=self.fortostoConn,
            schema=TestConfigurationProvider.schema,
            delimiter=',',
            tableNamePrefix='',
            primaryKey='id',
            filenamePattern='',
            dropTableIfExists=False,
            castNumbers=True,
            target='./testData/csv-2MB-1.csv',
            table=table,
            appendMode=False
        )
        engine.fortosto()

        count = self.dao.getRecordCountOfTable(schema=TestConfigurationProvider.schema, table=table)
        self.assertEqual(count, 33321)

        columnsInfo = self.dao.getColumnsInfoOfTable(schema=TestConfigurationProvider.schema, table=table)

        idInfo = next(item for item in columnsInfo if item["column_name"] == "id")
        self.assertEqual(idInfo['data_type'], 'integer')
        self.assertEqual(idInfo['is_identity'], True)

        firstdoseInfo = next(item for item in columnsInfo if item["column_name"] == "firstdose")
        self.assertEqual(firstdoseInfo['data_type'], 'integer')
        self.assertEqual(firstdoseInfo['is_identity'], False)



    # def tearDown(self):
    #     #print(f"droppping test table: {self.table}")
    #     #self.dao.dropTable(schema=TestConfigurationProvider.schema, tableName=self.table)
    #     pass

if __name__ == '__main__':
    unittest.main()
