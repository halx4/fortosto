import re
from .stringsNormalizer import StringsNormalizer
from .loggingUtils import getRootLogger

log = getRootLogger()


class TableNormalizer(object):

    @staticmethod
    def normalizeRecords(originalHeaders: list, newHeaders: list, records: list) -> list:
        newRecords = list()

        for oldRecord in records:  # each record is a dictionary. create a new dictionary with the new headers as keys
            newRecord = dict()
            for i in range(len(originalHeaders)):
                newRecord[newHeaders[i]] = oldRecord[originalHeaders[i]]
            newRecords.append(newRecord)

        return newRecords

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
        '''

        :param headersOriginal:
        :return:
        '''
        headers = headersOriginal.copy()
        currentlyNormalisedHeaders = set()

        # iterate headers with index
        for i in range(len(headers)):
            header = headers[i]
            log.trace("examining header: " + header)
            normalizedHeader = StringsNormalizer.normalizePgColumnName(header)
            log.trace("normalized header: " + normalizedHeader)

            dedupedNormalizedHeader = TableNormalizer.getDedupedHeaderName(normalizedHeader, currentlyNormalisedHeaders)

            headers[i] = dedupedNormalizedHeader
            currentlyNormalisedHeaders.add(dedupedNormalizedHeader)
        return headers

    @staticmethod
    def getDedupedHeaderName(header: str, otherHeaders: set) -> str:
        '''

        :param header:
        :param otherHeaders: the list of headers to dedup against
        :return:
        '''
        if (header not in otherHeaders):
            return header
        else:
            counter = 1
            while True:
                if f"{header}_{str(counter)}" in otherHeaders:
                    counter += 1
                else:
                    return f"{header}_{str(counter)}"
