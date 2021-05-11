import unittest
from datetime import datetime

from fortosto.commons.dateParser import DateParser


class Test(unittest.TestCase):

    def test_foo(self):
        result = DateParser.parseStrict('12/12/12')
        print(result)
        self.assertIsInstance(result, datetime)
        self.assertEqual(result, datetime(2012, 12, 12))

        result = DateParser.parseStrict('2021-01-30')
        print(result)
        self.assertIsInstance(result, datetime)
        self.assertEqual(result, datetime(2021, 1, 30))

        result = DateParser.parseStrict('2021-01')
        print(result)
        self.assertEqual(result, None)

        # DateParser.parse('Fri, 12 Dec 2014 10:55:50')
        # datetime.datetime(2014, 12, 12, 10, 55, 50)
        # dateparser.parse('Martes 21 de Octubre de 2014')  # Spanish (Tuesday 21 October 2014)
        # datetime.datetime(2014, 10, 21, 0, 0)
        # dateparser.parse('Le 11 Décembre 2014 à 09:00')  # French (11 December 2014 at 09:00)
        # datetime.datetime(2014, 12, 11, 9, 0)
        # dateparser.parse('13 января 2015 г. в 13:34')  # Russian (13 January 2015 at 13:34)
        # datetime.datetime(2015, 1, 13, 13, 34)
        # dateparser.parse('1 เดือนตุลาคม 2005, 1:00 AM')  # Thai (1 October 2005, 1:00 AM)
        # datetime.datetime(2005, 10, 1, 1, 0)


    def test_decodeValidToken(self):
        pass
        #self.assertRaises(jwt.exceptions.InvalidTokenError,decode,invalidToken)


if __name__ == '__main__':
    unittest.main()
