def getCastColumnToIntegerQuery(schema: str, table: str, column: str) -> str:
    query = f"""
    ALTER TABLE  "{schema}"."{table}"
    ALTER COLUMN "{column}" TYPE INTEGER USING NULLIF("{column}", '')::integer
    """
    return query


def getCastColumnToFloatQuery(schema: str, table: str, column: str) -> str:
    query = f"""
    ALTER TABLE  "{schema}"."{table}"
    ALTER COLUMN "{column}" TYPE FLOAT USING NULLIF("{column}", '')::float
    """
    return query


def getCreateTableQuery(schema: str, table: str, columns: list, idColumnName=None) -> str:
    query = f"""CREATE TABLE "{schema}"."{table}"
(
"""
    if idColumnName:
        query +=f"""    "{idColumnName}" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
        """


    query+=',\n'.join([f"""    "{column}" character varying""" for column in columns])

#     for column in columns:
#         query += f"""   {column} character varying,
# """

    if idColumnName:
        query += f"""
,CONSTRAINT "{table}_pkey" PRIMARY KEY ("{idColumnName}")"""

    query += """
);
"""

    return query


def getDropTableQuery(schema: str, table: str, ifExists: bool) -> str:
    ifExistsString = 'IF EXISTS ' if ifExists else ''
    query = f'DROP TABLE {ifExistsString}"{schema}"."{table}"'

    return query


def getTruncateTableQuery(schema: str, table: str, cascade: bool = False) -> str: # TODO test
    query = f'TRUNCATE "{schema}"."{table}"'
    if (cascade):
        query += f' CASCADE'

    return query