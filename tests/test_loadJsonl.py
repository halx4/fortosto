import unittest
from fortosto.commons.dao import DAO
from tests.TestConfigurationProvider import TestConfigurationProvider
import psycopg2
from fortosto.fortosto import Fortosto


class TestLoadJson(unittest.TestCase):

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

        self.table = "test_load_jsonl"

    def test_load(self):
        exists = self.dao.tableExists(schema=TestConfigurationProvider.schema, tableName=self.table)
        self.assertFalse(exists)

        engine = Fortosto(
            conn=self.fortostoConn,
            schema=TestConfigurationProvider.schema,
            delimiter=',',
            tableNamePrefix='',
            primaryKey='',
            filenamePattern='',
            dropTableIfExists=False,
            castNumbers=False,
            target='./testData/jsonl-9MB-1.jsonl',
            table=self.table,
        )
        engine.fortosto()

        count = self.dao.getRecordCountOfTable(schema=TestConfigurationProvider.schema, tableName=self.table)
        self.assertEqual(count, 33321)

    def tearDown(self):
        print(f"droppping test table: {self.table}")
        self.dao.dropTable(schema=TestConfigurationProvider.schema, tableName=self.table)


if __name__ == '__main__':
    unittest.main()
