import ntpath
import os

from unidecode import unidecode
import re


class StringsNormalizer(object):

    @staticmethod
    def filenameToNormalisedTableName(input: str) -> str:
        return os.path.splitext(ntpath.basename(input.lower()))[0] #TODO add tests for this method

    @staticmethod
    def normalizePgColumnName(input: str) -> str:
        # normalize non-ascii characters
        result = unidecode(input)

        result = result.lower()

        charactersToReplaceRegExp = "[ !\"£$%^&*()+{}:@~?><|¬\\\\,./;\'#\\][=\\-`]"
        result = re.sub(charactersToReplaceRegExp, '_', result)

        if result[0].isdigit():
            result = "_" + result

        return result
