import unittest
from commons.TableNormalizer import TableNormalizer
from commons.dao import DAO
from tests.TestConfigurationProvider import TestConfigurationProvider
import psycopg2


class TestTableNormalizer(unittest.TestCase):

    def test_createTable(self):
        print(TestConfigurationProvider.host)
        print(TestConfigurationProvider.port)
        print(TestConfigurationProvider.schema)
        print(TestConfigurationProvider.user)
        print(TestConfigurationProvider.password)

        conn = psycopg2.connect(
            dbname=TestConfigurationProvider.dbname,
            user=TestConfigurationProvider.user,
            password=TestConfigurationProvider.password,
            host=TestConfigurationProvider.host,
            port=TestConfigurationProvider.port
        )

        dao = DAO.fromConnection(conn, False)

        dao.createVarCharTable(schema=TestConfigurationProvider.schema, tableName="foo",
                               columns=['c1', 'c2', 'c3'])

        dao.dropTable(schema=TestConfigurationProvider.schema, tableName="foo")


if __name__ == '__main__':
    unittest.main()
