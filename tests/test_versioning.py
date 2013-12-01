import sys, os

# add scripts dir to sys.path
script_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'LP_versioning'))

sys.path.append(script_dir)

from LP_versioning import *
import unittest
from collections import namedtuple

MockFont = namedtuple("MockFont", ['path'])

class TestExtractVersionFromFilename(unittest.TestCase):
    def test_itExtractVersionNumbersFromValidFilenames(self):
        self.assertEqual(1, extractVersionFromFilename('name-A001'))
        self.assertEqual(12, extractVersionFromFilename('name-Z012'))

    def test_itReturnsMinusOneFromInvalidFormats(self):
        self.assertEqual(-1, extractVersionFromFilename('name-a001'))
        self.assertEqual(-1, extractVersionFromFilename('name-A01'))
        self.assertEqual(-1, extractVersionFromFilename('nameA001'))
        self.assertEqual(-1, extractVersionFromFilename('-A001'))


class TestGetFontVersionState(unittest.TestCase):
    def assertFailure(self, result, expectedErrorMessage):
        print "result", result
        self.assertTrue(result[0] is False)
        self.assertEqual(result[1], expectedErrorMessage)

    def test_itValidatesPresenceOfFont(self):
        result = getFontState(None)
        self.assertFailure(result, "there is no open font")

    def test_itValidatesFormatOfFilename(self):
        result = getFontState(MockFont(path="/bla/file-b0001.ufo"))
        self.assertFailure(result, "font filename 'file-b0001' is invalid")


def main():
    unittest.main()

if __name__ == '__main__':
    main()