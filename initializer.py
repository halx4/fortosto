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

    parser.add_argument('-f', '--target', type=str, help="target file name (default: lowercased file name)", required=True)
    parser.add_argument('-s', '--schema', type=str, help="The schema name", default=os.environ.get("FST_SCHEMA","public"), required=False)
    parser.add_argument('-d', '--database', type=str, help="The db name", default=os.environ.get("FST_DB", "postgres"), required=False)
    parser.add_argument('-H', '--host', type=str, help="Db Host", default=os.environ.get("FST_HOST", "localhost"), required=False)
    parser.add_argument('-P', '--port', type=int, help="TCP Port", default=os.environ.get("FST_PORT", 5432), required=False)
    parser.add_argument('-u', '--username', type=str, help="Db username", default=os.environ.get("FST_USERNAME", "postgres"), required=False)
    parser.add_argument('-p', '--password', type=str, help="Db password", default=os.environ.get("FST_PASSWORD", ""), required=False)
    parser.add_argument('-t', '--table', type=str, help="table name (must match [a-z0-9_]* )(default: the filename lowercased and normalised)", default=os.environ.get("FST_TABLE", ""), required=False)
    parser.add_argument('-D', '--delimiter', type=str, help="delimiter (default: ',')", default=os.environ.get("FST_DELIMITER", ","), required=False)
    parser.add_argument('-tp', '--table-prefix', type=str, help="table name prefix", default=os.environ.get("FST_TABLE_NAME_PREFIX", ""), required=False)
    parser.add_argument('-pk', '--primary-key', type=str, help="primary key column name to be added", default=os.environ.get("FST_PRIMARY_KEY", ""), required=False)

    parser.add_argument('--filename-pattern', type=str, help="Glob-style lookup pattern.\n Ignored when the target is file.(default: '*.csv')", default=os.environ.get("FST_FILENAME_PATTERN", "*.csv"), required=False)
    parser.add_argument('--drop-if-exists', help="drop table if it already exists", action='store_true', required=False)
    parser.add_argument('--cast-numbers', help="try casting number columns after importing", action='store_true', required=False)
    parser.add_argument('--verbose', help="verbose logging", action='store_true', required=False)

    parser.add_argument('-v', '--version', help="print version info", action='version', version=f'fortosto v.{Properties.applicationVersion}')
    # dry run
    # atomic

    # @formatter:on

    args = parser.parse_args()

    Properties.target = args.target
    Properties.schema = args.schema
    Properties.dbname = args.database
    Properties.host = args.host
    Properties.port = args.port
    Properties.user = args.username
    Properties.password = args.password
    Properties.tableNamePrefix = args.table_prefix
    Properties.primaryKey = args.primary_key

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
    dbname=\t\t\t\t{Properties.dbname}
    schema=\t\t\t\t{Properties.schema}
    host=\t\t\t\t{Properties.host}
    port=\t\t\t\t{Properties.port}
    user=\t\t\t\t{Properties.user}
    target=\t\t\t\t{Properties.target}
    filenamePattern=\t{Properties.filenamePattern}
    delimiter=\t\t\t{Properties.delimiter}
    [prefix]table=\t\t{Properties.tableNamePrefix}{Properties.table}
    dropTableIfExists=\t{Properties.dropTableIfExists}
    castNumbers=\t\t{Properties.castNumbers}
    primaryKey=\t\t{Properties.primaryKey}
    verboseLogging=\t\t{Properties.verboseLogging}
    """)

    log.trace("password=\t\t{Properties.password}")

    # configure logging
    if Properties.verboseLogging:
        loggingUtils.setLevel(VERBOSE_LOG_LEVEL)

    return


if __name__ == '__main__':
    initialize()
