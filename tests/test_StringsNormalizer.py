import unittest

from unidecode import unidecode

from fortosto.commons.stringsNormalizer import StringsNormalizer


class Test(unittest.TestCase):

    def test_spaces(self):
        input = "kot _lot"
        expected = "kot__lot"
        result = StringsNormalizer.normalizePgColumnName(input)
        self.assertEqual(result, expected)

    def test_CapitalLetters(self):
        input = "Is the value true?24"
        expected = "is_the_value_true_24"
        result = StringsNormalizer.normalizePgColumnName(input)
        self.assertEqual(result, expected)

    def test_3(self):
        input = "Is the value true?24"
        expected = "is_the_value_true_24"
        result = StringsNormalizer.normalizePgColumnName(input)
        self.assertEqual(result, expected)

    def test_unidecode(self):
        import string
        normalisedCharSet = string.ascii_letters + string.digits + string.punctuation + ' '  # space character is included in the set
        print(f"normalisedCharSet: {normalisedCharSet}")
        normalisedCharSet = set(normalisedCharSet)

        specialChars = ['Ç', 'ü', 'é', 'â', 'ä', 'à', 'å', 'ç', 'ê', 'ë', 'è', 'ï', 'î', 'ì', 'æ', 'Æ', 'ô', 'ö', 'ò',
                        'û', 'ù', 'ÿ', '¢', '£', '¥', 'P', 'ƒ', 'á', 'í', 'ó', 'ú', 'ñ', 'Ñ', '‡', '‡', '¿', '¬', '½',
                        '¼', '¡', '«', '»', '¦', 'ß', 'µ', '±', '°', '•', '·', '²', '€', '„', '…', '†', '‡', 'ˆ', '‰',
                        'Š', '‹', 'Œ', '‘', '’', '“', '”', '–', '—', '˜', '™', 'š', '›', 'œ', 'Ÿ', '¨', '©', '®', '¯',
                        '³', '´', '¸', '¹', '¾', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï',
                        'Ð', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ã', 'ð', 'õ', '÷', 'ø',
                        'ü', 'ý', 'þ']
        for ch in specialChars:
            unidecoded = unidecode(ch)
            print(ch + " -> " + unidecoded)
            self.assertTrue(set(unidecoded).issubset(normalisedCharSet))


if __name__ == '__main__':
    unittest.main()
