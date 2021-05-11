import os


class TestConfigurationProvider():

    dbname = os.environ.get("TEST_FST_DBNAME", "postgres")
    user = os.environ.get("TEST_FST_USER", "postgres")
    password = os.environ.get("TEST_FST_PASSWORD")
    host = os.environ.get("TEST_FST_HOST", "localhost")
    port = os.environ.get("TEST_FST_PORT", 5432)

    schema = os.environ.get("TEST_FST_SCHEMA", "public")
