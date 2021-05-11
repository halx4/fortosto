import unittest
from commons.TableNormalizer import TableNormalizer


class TestTableNormalizer(unittest.TestCase):

    def test_simple(self):
        headers = ["header1", "header2", "header3", "header4", "header5"]
        expected = ["header1", "header2", "header3", "header4", "header5"]

        result = TableNormalizer.normalizeHeaders(headers)
        self.assertEqual(result, expected)

    def test_2(self):
        headers = ["header1", "header1", "Header3", "header4", "header5"]
        expected = ["header1", "header1_1", "header3", "header4", "header5"]

        result = TableNormalizer.normalizeHeaders(headers)
        self.assertEqual(result, expected)

    def test_3(self):
        headers = ["header", "header", "Header", "HEADER", "HEADER_3"]
        expected = ["header", "header_1", "header_2", "header_3", "header_3_1"]

        result = TableNormalizer.normalizeHeaders(headers)
        self.assertEqual(result, expected)

    def test_3(self):
        headers = ["header1", "HEADER1", "Header3"]
        records = [
            {"header1": "v1a", "HEADER1": "v2a", "Header3": "v3a"},
            {"header1": "v1b", "HEADER1": "v2b", "Header3": "v3b"},
            {"header1": "v1c", "HEADER1": "v2c", "Header3": "v3c"},
        ]

        expectedHeaders = ["header1", "header1_1", "header3"]
        expectedRecords = [
            {"header1": "v1a", "header1_1": "v2a", "header3": "v3a"},
            {"header1": "v1b", "header1_1": "v2b", "header3": "v3b"},
            {"header1": "v1c", "header1_1": "v2c", "header3": "v3c"},
        ]

        (resultHeaders, resultRecords) = TableNormalizer.normalizeHeadersForTable(headers,records)

        self.assertEqual(resultHeaders, expectedHeaders)
        self.assertEqual(resultRecords, expectedRecords)



if __name__ == '__main__':
    unittest.main()
