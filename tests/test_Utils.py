import unittest
from commons.TableNormalizer import TableNormalizer
from commons.Utils import getLowercasedFilenameExtension
from commons.dao import DAO
from properties import Properties


class TestUtils(unittest.TestCase):

    def test_getLowercasedFilenameExtension(self):

        result = getLowercasedFilenameExtension( "foo.txt")
        self.assertEqual(".txt",result)

        result = getLowercasedFilenameExtension("foo.bar.kot")
        self.assertEqual(".kot", result)


if __name__ == '__main__':
    unittest.main()
