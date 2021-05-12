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

    def test_columnInfoWithoutId(self):
        table = "columnInfo"

        self.dao.dropTable(schema=TestConfigurationProvider.schema, tableName=table)
        self.dao.createVarCharTable(schema=TestConfigurationProvider.schema, tableName=table,
                                    columns=['c1', 'c2'])

        result = self.dao.getColumnsInfoOfTable(schema=TestConfigurationProvider.schema, tableName=table)

        c1Info = next(item for item in result if item["column_name"] == "c1")
        self.assertEqual(c1Info['data_type'], 'character varying')
        self.assertEqual(c1Info['ordinal_position'], 1)
        self.assertEqual(c1Info['is_nullable'], True)
        self.assertEqual(c1Info['is_identity'], False)

    def test_columnInfoWithId(self):
        table = "columnInfo"

        self.dao.dropTable(schema=TestConfigurationProvider.schema, tableName=table)
        self.dao.createVarCharTable(schema=TestConfigurationProvider.schema, tableName=table,
                                    columns=['c1', 'c2'],
                                    idColumn='id')

        result = self.dao.getColumnsInfoOfTable(schema=TestConfigurationProvider.schema, tableName=table)

        idInfo = next(item for item in result if item["column_name"] == "id")
        self.assertEqual(idInfo['data_type'], 'integer')
        self.assertEqual(idInfo['ordinal_position'], 1)
        self.assertEqual(idInfo['is_nullable'], False)
        self.assertEqual(idInfo['is_identity'], True)

        c1Info = next(item for item in result if item["column_name"] == "c1")
        self.assertEqual(c1Info['data_type'], 'character varying')
        self.assertEqual(c1Info['ordinal_position'], 2)
        self.assertEqual(c1Info['is_nullable'], True)
        self.assertEqual(c1Info['is_identity'], False)


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
