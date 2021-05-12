import unittest
from fortosto.commons.TableNormalizer import TableNormalizer
from fortosto.commons.Utils import getLowercasedFilenameExtension
from fortosto.commons.dao import DAO
from fortosto.properties import Properties


class TestUtils(unittest.TestCase):

    def test_getLowercasedFilenameExtension(self):

        result = getLowercasedFilenameExtension( "foo.txt")
        self.assertEqual(".txt",result)

        result = getLowercasedFilenameExtension("foo.bar.kot")
        self.assertEqual(".kot", result)


if __name__ == '__main__':
    unittest.main()
