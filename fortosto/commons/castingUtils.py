from __future__ import annotations

from .CastDataType import CastDataType
from .dao import DAO
from .loggingUtils import getRootLogger

log = getRootLogger()


def tryCastingHeaders(dao: DAO, schema: str, table: str, columns: list):
    castResults = dict()
    for header in columns:
        castResult = tryCastingColumn(dao, schema, table, header)
        if castResult is not None:
            castResults[header] = str(castResult.name)

    log.info('conversions made:')
    log.info(castResults)
    return castResults


def tryCastingColumn(dao: DAO, schema: str, table: str, header: str) -> CastDataType | None:
    log.debug(f"attempting cast column {header}")
    ### integer
    try:
        log.debug("> casting to  Integer...")
        dao.castColumnToInteger(schema, table, header)
        log.debug("> casting to  Integer succeeded")
        return CastDataType.Integer
    except Exception as e:
        log.debug("> casting to  Integer failed")

    ### double
    try:
        log.debug("> casting to  Float...")
        dao.castColumnToFloat(schema, table, header)
        log.debug("> casting to  Float succeeded")
        return CastDataType.Double
    except Exception as e:
        log.debug("> casting to  Float failed")

    ### date
    # TODO

    return None
