import argparse
import os

from commons import loggingUtils
from commons.stringsNormalizer import StringsNormalizer
from properties import Properties
import ntpath
from commons.loggingUtils import getRootLogger, VERBOSE_LOG_LEVEL

log = getRootLogger()


def initialize():
    #@formatter:off
    parser = argparse.ArgumentParser(description='Imports csv data to Postgres DB',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f', '--filename', type=str, help="CSV File name(default: lowercased file name)", required=True)
    parser.add_argument('-s', '--schema', type=str, help="The schema name", default=os.environ.get("P2C_SCHEMA","public"), required=False)
    parser.add_argument('-d', '--database', type=str, help="The db name", default=os.environ.get("P2C_DB", "postgres"), required=False)
    parser.add_argument('-H', '--host', type=str, help="Db Host", default=os.environ.get("P2C_HOST", "localhost"), required=False)
    parser.add_argument('-P', '--port', type=int, help="TCP Port", default=os.environ.get("P2C_PORT", 5432), required=False)
    parser.add_argument('-u', '--username', type=str, help="Db username", default=os.environ.get("P2C_USERNAME", "postgres"), required=False)
    parser.add_argument('-p', '--password', type=str, help="Db password", default=os.environ.get("P2C_PASSWORD", ""), required=False)
    parser.add_argument('-t', '--table', type=str, help="table name (must match [a-z0-9_]* )(default: the filename lowercased and normalised)", default=os.environ.get("P2C_TABLE", ""), required=False)
    parser.add_argument('-D', '--delimiter', type=str, help="delimiter (default: ',')", default=os.environ.get("P2C_DELIMITER", ","), required=False)
    parser.add_argument('--table-prefix', type=str, help="table name prefix", default=os.environ.get("P2C_TABLE_NAME_PREFIX", ""), required=False)

    parser.add_argument('--filename-pattern', type=str, help="Glob-style lookup pattern. Ignored when the target is file.(default: '*.csv')", default=os.environ.get("P2C_FILENAME_PATTERN", "*.csv"), required=False)
    parser.add_argument('--drop-if-exists', help="drop table if it already exists", action='store_true', required=False)
    parser.add_argument('--cast-numbers', help="try casting number columns after importing", action='store_true', required=False)
    parser.add_argument('--verbose', help="verbose logging", action='store_true', required=False)

    parser.add_argument('-v', '--version', help="print version info", action='version', version=f'P2G v.{Properties.applicationVersion}')
    # dry run
    # atomic
    # skip primary key
    # custom primary key column name

    # @formatter:on

    args = parser.parse_args()

    Properties.filename = args.filename
    Properties.schema = args.schema
    Properties.dbname = args.database
    Properties.host = args.host
    Properties.port = args.port
    Properties.user = args.username
    Properties.password = args.password
    Properties.tableNamePrefix = args.table_prefix

    if args.table:
        Properties.table = args.table
    else:
        Properties.table = StringsNormalizer.filenameToNormalisedTableName(args.filename)

    Properties.delimiter = args.delimiter
    Properties.filenamePattern = args.filename_pattern
    Properties.dropTableIfExists = args.drop_if_exists
    Properties.castNumbers = args.cast_numbers
    Properties.verboseLogging = args.verbose

    log.debug(f"""
    schema=\t\t{Properties.schema}
    dbname=\t\t{Properties.dbname}
    user=\t\t{Properties.user}
    password=\t{Properties.password}
    host=\t\t{Properties.host}
    port=\t\t{Properties.port}
    filename=\t{Properties.filename}
    [prefix]table=\t\t{Properties.tableNamePrefix}{Properties.table}
    delimiter=\t{Properties.delimiter}
    filenamePattern=\t{Properties.filenamePattern}
    dropTableIfExists=\t{Properties.dropTableIfExists}
    castNumbers=\t{Properties.castNumbers}
    verboseLogging=\t{Properties.verboseLogging}
    """)

    # configure logging
    if Properties.verboseLogging:
        loggingUtils.setLevel(VERBOSE_LOG_LEVEL)

    return


if __name__ == '__main__':
    initialize()
