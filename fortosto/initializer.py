import argparse
import os

from .commons import loggingUtils
from .commons.InitializationResult import InitializationResult
from .commons.stringsNormalizer import StringsNormalizer
from .properties import Properties
from .commons.loggingUtils import getRootLogger, VERBOSE_LOG_LEVEL
import ntpath

log = getRootLogger()


def initialize() -> InitializationResult:

    #@formatter:off
    parser = argparse.ArgumentParser(description='Imports csv data to Postgres DB',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f', '--target', type=str, help="target file name (default: lowercased file name)", required=True)
    parser.add_argument('-H', '--host', type=str, help="Db Host", default=os.environ.get("FST_HOST", "localhost"), required=False)
    parser.add_argument('-P', '--port', type=int, help="TCP Port", default=os.environ.get("FST_PORT", 5432), required=False)
    parser.add_argument('-u', '--username', type=str, help="Db username", default=os.environ.get("FST_USERNAME", "postgres"), required=False)
    parser.add_argument('-p', '--password', type=str, help="Db password", default=os.environ.get("FST_PASSWORD", ""), required=False)
    parser.add_argument('-d', '--database', type=str, help="The db name", default=os.environ.get("FST_DB", "postgres"), required=False)
    parser.add_argument('-s', '--schema', type=str, help="The schema name", default=os.environ.get("FST_SCHEMA","public"), required=False)
    parser.add_argument('-t', '--table', type=str, help="table name (must match [a-zA-Z0-9_]* )(default: the filename lowercased and normalised)", default=os.environ.get("FST_TABLE", ""), required=False)
    parser.add_argument('-D', '--delimiter', type=str, help="delimiter (default: ',')", default=os.environ.get("FST_DELIMITER", ","), required=False)
    parser.add_argument('-tp', '--table-prefix', type=str, help="table name prefix", default=os.environ.get("FST_TABLE_NAME_PREFIX", ""), required=False)
    parser.add_argument('-pk', '--primary-key', type=str, help="primary key column name to be added", default=os.environ.get("FST_PRIMARY_KEY", ""), required=False)

    parser.add_argument('--filename-pattern', type=str, help="Glob-style lookup pattern.\n Ignored when the target is file.", default=os.environ.get("FST_FILENAME_PATTERN", "*.*"), required=False)
    parser.add_argument('-die', '--drop-if-exists', help="drop table if it already exists", action='store_true', required=False)
    parser.add_argument('--append', help="append to an existing table and do not create new one", action='store_true', required=False)
    parser.add_argument('--cast-numbers', help="try casting number columns after importing", action='store_true', required=False)
    parser.add_argument('--verbose', help="verbose logging", action='store_true', required=False)

    parser.add_argument('-v', '--version', help="print version info", action='version', version=f'fortosto v.{Properties.applicationVersion}')

    # @formatter:on

    args = parser.parse_args()

    result = InitializationResult()

    result.target = args.target
    result.schema = args.schema
    result.dbname = args.database
    result.host = args.host
    result.port = args.port
    result.user = args.username
    result.password = args.password
    result.tableNamePrefix = args.table_prefix
    result.primaryKey = args.primary_key

    if args.table:
        result.table = args.table
    else:
        result.table = StringsNormalizer.filenameToNormalisedTableName(args.target)

    result.delimiter = args.delimiter
    result.filenamePattern = args.filename_pattern
    result.dropTableIfExists = args.drop_if_exists
    result.castNumbers = args.cast_numbers
    result.appendMode = args.append

    result.verboseLogging = args.verbose

    log.debug(f"""
    dbname=\t\t\t\t{result.dbname}
    schema=\t\t\t\t{result.schema}
    host=\t\t\t\t{result.host}
    port=\t\t\t\t{result.port}
    user=\t\t\t\t{result.user}
    target=\t\t\t\t{result.target}
    filenamePattern=\t{result.filenamePattern}
    delimiter=\t\t\t{result.delimiter}
    [prefix]table=\t\t{result.tableNamePrefix}{result.table}
    dropTableIfExists=\t{result.dropTableIfExists}
    castNumbers=\t\t{result.castNumbers}
    primaryKey=\t\t{result.primaryKey}
    verboseLogging=\t\t{result.verboseLogging}
    """)

    log.trace(f"password=\t\t{result.password}")

    # TODO move this somewhere else
    # configure logging
    if result.verboseLogging:
        loggingUtils.setLevel(VERBOSE_LOG_LEVEL)

    return result


if __name__ == '__main__':
    initialize()
