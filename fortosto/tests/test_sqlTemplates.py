import unittest

from commons.sqlTemplates import getCreateTableQuery


class TestSqlTemplates(unittest.TestCase):

    def test_sql1(self):
        expected = """CREATE TABLE "theSchema"."theTable"
(
    "c1" character varying,
    "c2" character varying,
    "c3" character varying
);
"""
        result = getCreateTableQuery(schema='theSchema', table='theTable', columns=['c1', 'c2', 'c3'], idColumnName='')
        print(result)
        #        print(expected)

        self.assertEqual(result, expected)

    def test_sql2(self):
        expected = """CREATE TABLE "theSchema"."theTable"
(
    "id" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
            "c1" character varying,
    "c2" character varying,
    "c3" character varying
,CONSTRAINT "theTable_pkey" PRIMARY KEY ("id")
);
"""
        result = getCreateTableQuery(schema='theSchema', table='theTable', columns=['c1', 'c2', 'c3'],
                                     idColumnName='id')
        print(result)
        #        print(expected)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
