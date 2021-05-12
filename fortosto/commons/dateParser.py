import dateparser
from .loggingUtils import getRootLogger

log = getRootLogger()


class DateParser(object):

    @staticmethod
    def parseStrict(inputStr: str):
        return dateparser.parse(inputStr, settings={'STRICT_PARSING': True})
