import unittest
import re


class TestMain(unittest.TestCase):

    def test_foo(self):
        mylist = ["dog", "uncats","cat" ,"wildcat", "thundercat", "cow", "hooo"]
        r = re.compile("^.*cat$")
        newlist = list(filter(r.match, mylist))  # Read Note
        print(newlist)

        pass
#        self.assertEqual(payload, decoded)


    def test_decodeValidToken(self):
        pass
        #self.assertRaises(jwt.exceptions.InvalidTokenError,decode,invalidToken)


if __name__ == '__main__':
    unittest.main()
