import unittest
from commons.TableNormalizer import TableNormalizer
from commons.dao import DAO
from properties import Properties


class TestTableNormalizer(unittest.TestCase):

    def test_createTable(self):
        dao = DAO(False)

        result = dao.createVarCharTable("playground", "foo")
        print(result)


if __name__ == '__main__':
    unittest.main()
