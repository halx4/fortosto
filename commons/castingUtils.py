from __future__ import annotations

from commons.CastDataType import CastDataType
from commons.dao import DAO
from properties import Properties
from commons.loggingUtils import getRootLogger

log = getRootLogger()


def tryCastingHeaders(dao: DAO, columns: list):
    castResults = dict()
    for header in columns:
        castResult = tryCastingColumn(dao, header)
        if castResult is not None:
            castResults[header] = str(castResult.name)

    log.info('conversions made:')
    log.info(castResults)
    return castResults


def tryCastingColumn(dao: DAO, header: str) -> CastDataType|None:
    log.debug(f"attempting cast column {header}")
    ### integer
    try:
        log.debug("> casting to  Integer...")
        dao.castColumnToInteger(Properties.schema, Properties.table, header)
        log.debug("> casting to  Integer succeeded")
        return CastDataType.Integer
    except Exception as e:
        log.debug("> casting to  Integer failed")

    ### double
    try:
        log.debug("> casting to  Float...")
        dao.castColumnToFloat(Properties.schema, Properties.table, header)
        log.debug("> casting to  Float succeeded")
        return CastDataType.Double
    except Exception as e:
        log.debug("> casting to  Float failed")

    ### date
    # TODO

    return None
