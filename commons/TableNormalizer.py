import re
from commons.stringsNormalizer import StringsNormalizer
from commons.loggingUtils import getRootLogger

log = getRootLogger()


class TableNormalizer(object):

    @staticmethod
    def normalizeHeadersForTable(originalHeaders: list, records: list) -> tuple:
        newHeaders = TableNormalizer.normalizeHeaders(originalHeaders)
        newRecords = list()

        for oldRecord in records:  # each record is a dictionary. create a new dictionary with the new headers as keys
            newRecord = dict()
            for i in range(len(originalHeaders)):
                newRecord[newHeaders[i]] = oldRecord[originalHeaders[i]]
            newRecords.append(newRecord)

        return (newHeaders, newRecords)

    @staticmethod
    def normalizeHeaders(headersOriginal: list):
        headers = headersOriginal.copy()
        # iterate headers with index
        for i in range(len(headers)):
            header = headers[i]
            log.debug("examining header: " + header)
            normalizedHeader = StringsNormalizer.normalizePgColumnName(header)
            log.debug("normalized header: " + normalizedHeader)

            otherHeaders = headers[:i]

            dedupedNormalizedHeader = TableNormalizer.getDedupedHeaderName(normalizedHeader, otherHeaders)

            headers[i] = dedupedNormalizedHeader
        return headers

    @staticmethod
    def getDedupedHeaderName(normalizedHeader: str, otherHeaders: list) -> str:
        if (normalizedHeader not in otherHeaders):
            return normalizedHeader
        else:
            counter = 1
            while True:
                if f"{normalizedHeader}_{str(counter)}" in otherHeaders:
                    counter += 1
                else:
                    return f"{normalizedHeader}_{str(counter)}"
