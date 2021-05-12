import unittest
from fortosto.commons.TableNormalizer import TableNormalizer
from fortosto.commons.dao import DAO
from tests.TestConfigurationProvider import TestConfigurationProvider
import psycopg2


class TestDao(unittest.TestCase):

    def setUp(self):
        conn = psycopg2.connect(
            dbname=TestConfigurationProvider.dbname,
            user=TestConfigurationProvider.user,
            password=TestConfigurationProvider.password,
            host=TestConfigurationProvider.host,
            port=TestConfigurationProvider.port
        )

        self.dao = DAO.fromConnection(conn, False)

    def test_count(self):
        table = "test_count"

        exists = self.dao.tableExists(schema=TestConfigurationProvider.schema, tableName=table)
        self.assertFalse(exists)

        # create empty table
        self.dao.createVarCharTable(schema=TestConfigurationProvider.schema, tableName=table,
                                    columns=['c1', 'c2'])
        exists = self.dao.tableExists(schema=TestConfigurationProvider.schema, tableName=table)
        self.assertTrue(exists)

        count = self.dao.getRecordCountOfTable(
            schema=TestConfigurationProvider.schema,
            tableName=table)
        self.assertEqual(count, 0)

        # populate the table with some records
        records = [{'c1': '1', 'c2': '2'}, {'c1': '3', 'c2': '4'}, {'c1': 'a', 'c2': 'b'}]

        self.dao.saveRecordsToDb(schema=TestConfigurationProvider.schema,
                                 table=table,
                                 recordsAsList=records)

        count = self.dao.getRecordCountOfTable(
            schema=TestConfigurationProvider.schema,
            tableName=table)
        self.assertEqual(count, 3)

        # drop the table
        self.dao.dropTable(schema=TestConfigurationProvider.schema, tableName=table)

        exists = self.dao.tableExists(schema=TestConfigurationProvider.schema, tableName=table)
        self.assertFalse(exists)




if __name__ == '__main__':
    unittest.main()
