def getCreateTableQuery(schema: str, table: str, columns: list) -> str:
    query = f"""CREATE TABLE {schema}.{table}
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
"""
    for column in columns:
        query += f"{column} character varying,"

    query += f"""CONSTRAINT {table}_pkey PRIMARY KEY (id)
);
"""

    return query
