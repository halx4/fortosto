from unidecode import unidecode
import re


class StringsNormalizer(object):

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
