import sys, os

# add scripts dir to sys.path
script_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'LP_versioning'))

sys.path.append(script_dir)

from LP_versioning import *
import unittest
import os

class MockFont(object):
    def __init__(self, path=None, info=None):
        self.path = path
        self.info = info

    def save(self, path):
        self.path = path
        pass

class MockInfo(object):
    def __init__(self, versionMinor=None, note=None):
        self.versionMinor = versionMinor
        self.note = note


class TestExtractVersionFromFilename(unittest.TestCase):
    def test_itExtractVersionNumbersFromValidFilenames(self):
        self.assertEqual(1, extractVersionFromFilename('name-A001'))
        self.assertEqual(12, extractVersionFromFilename('name-Z012'))
        self.assertEqual(12, extractVersionFromFilename('jung-regular-Z012'))

    def test_itReturnsMinusOneForInvalidFormats(self):
        self.assertEqual(-1, extractVersionFromFilename('name-a001'))
        self.assertEqual(-1, extractVersionFromFilename('name-A01'))
        self.assertEqual(-1, extractVersionFromFilename('nameA001'))
        self.assertEqual(-1, extractVersionFromFilename('-A001'))


class TestGetFontVersionState(unittest.TestCase):
    def assertFailure(self, result, expectedErrorMessage):
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

    def test_itValidatesNextVersionOfFileDoesNotExist(self):
        realPathExists = os.path.exists
        os.path.exists = lambda x : True

        info = MockInfo(versionMinor=1)
        font = MockFont(path="/bla/file-B001.ufo", info=info)

        result = getFontState(font)
        self.assertFailure(result, "the next font already exists /bla/file-B002.ufo")

        os.path.exists = realPathExists

    def test_itReturnsAFontStateObjectIfAllValidationsPass(self):
        realPathExists = os.path.exists
        os.path.exists = lambda x : False

        info = MockInfo(versionMinor=1)
        font = MockFont(path="/bla/file-B001.ufo", info=info)

        result = getFontState(font)
        expected = FontState(fullPath="/bla/file-B001.ufo",
                             directory="/bla", 
                             basename="file-B", 
                             versionMinor=1)
        self.assertEqual(result[1], expected)

        os.path.exists = realPathExists

class TestCommitVersion(unittest.TestCase):
    def test_itIncrementsVersionMinorOfFontArgument(self):
        info = MockInfo(versionMinor=1, note="changelogMessage here")
        font = MockFont(path="/bla/file-B001.ufo", info=info)
        fontState = FontState(fullPath="/bla/file-B001.ufo",
                              directory="/bla", 
                              basename="file-B", 
                              versionMinor=1)
        commitVersion(font, fontState, False)
        self.assertEqual(font.info.versionMinor, 2)

    def test_itClearsInfoNote(self):
        info = MockInfo(versionMinor=1, note="changelogMessage here")
        font = MockFont(path="/bla/file-B001.ufo", info=info)
        fontState = FontState(fullPath="/bla/file-B001.ufo",
                              directory="/bla", 
                              basename="file-B", 
                              versionMinor=1)
        commitVersion(font, fontState, False)
        self.assertEqual(font.info.note, None)

    def test_itSavesTheFontWithTheIncrementedName(self):
        info = MockInfo(versionMinor=1, note="changelogMessage here")
        font = MockFont(path="/bla/file-B001.ufo", info=info)
        fontState = FontState(fullPath="/bla/file-B001.ufo",
                              directory="/bla", 
                              basename="file-B", 
                              versionMinor=1)
        commitVersion(font, fontState, False)
        self.assertEqual(font.path, "/bla/file-B002.ufo")


def main():
    unittest.main()

if __name__ == '__main__':
    main()