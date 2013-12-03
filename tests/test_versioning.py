import sys, os

# add scripts dir to sys.path
script_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'LP_versioning'))

sys.path.append(script_dir)

from LP_versioning import *
import unittest
from collections import namedtuple

MockFont_T = namedtuple("MockFont_T", ['path', 'info'])
MockInfo_T = namedtuple("MockInfo_T", ['versionMinor', 'note'])

def MockFont(path=None, info=None):
    return MockFont_T(path, info)

def MockInfo(versionMinor=None, note=None):
    return MockInfo_T(versionMinor, note)

class TestExtractVersionFromFilename(unittest.TestCase):
    def test_itExtractVersionNumbersFromValidFilenames(self):
        self.assertEqual(1, extractVersionFromFilename('name-A001'))
        self.assertEqual(12, extractVersionFromFilename('name-Z012'))

    def test_itReturnsMinusOneForInvalidFormats(self):
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

    def test_itValidatesFontInfoMinorEqualsFilenameVersion(self):
        info = MockInfo(versionMinor=2)
        font = MockFont(path="/bla/file-B001.ufo", info=info)
        result = getFontState(font)
        self.assertFailure(result, "filename version(1) out of sync with info.versionMinor(2)")

    def test_itValidatesFontInfoNoteIsNotBlank(self):
        info = MockInfo(versionMinor=1, note="")
        font = MockFont(path="/bla/file-B001.ufo", info=info)
        result = getFontState(font)
        self.assertFailure(result, "font info note is blank, please write a changelogMessage")


def main():
    unittest.main()

if __name__ == '__main__':
    main()