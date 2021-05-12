import unittest
from fortosto.commons.TableNormalizer import TableNormalizer
from fortosto.commons.dao import DAO
from tests.TestConfigurationProvider import TestConfigurationProvider
import psycopg2


class TestTableNormalizer(unittest.TestCase):

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

        self.dao.getRecordsCountOfTable(
            schema=TestConfigurationProvider.schema,
            tableName="ext_test")

    def test_createTable(self):

        self.dao.createVarCharTable(schema=TestConfigurationProvider.schema, tableName="foo",
                               columns=['c1', 'c2', 'c3'])

        self.dao.dropTable(schema=TestConfigurationProvider.schema, tableName="foo")


if __name__ == '__main__':
    unittest.main()
