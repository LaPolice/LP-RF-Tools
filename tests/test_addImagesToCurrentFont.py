import sys, os

# add scripts dir to sys.path
scripts_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'scripts'))

sys.path.append(scripts_dir)

from addImagesToCurrentFont import parseFiles
import unittest



class TestParseDirectory(unittest.TestCase):

    fullPath = "/home/user/robo/images/"

    def test_itReturnsADictionary(self):
        result = parseFiles(self.fullPath, [])
        self.assertTrue( isinstance(parseFiles(self.fullPath,[]), 
                                    dict))


    def test_itFiltersInvalidFileExtensions(self):
    	fileList = ["lc-b.txt",
    				"lc-a.doc",
    				"lc-a.ai"]
    	result = parseFiles(self.fullPath, fileList)
    	self.assertEquals(len(result), 0)


    def test_itHandlesNumbers(self):
        fileList = ["num-0.png",
                    "num-10.png"]
        result = parseFiles(self.fullPath, fileList)
        self.assertEquals(result, {"zero": "/home/user/robo/images/num-0.png"})
        

    def test_itHandlesLowerCaseLetters(self):
        fileList = ["lc-b.png",
                    "lC-A.png",
                    "lc-bob.png"]
        result = parseFiles(self.fullPath, fileList)
        self.assertEquals(result, {"b": "/home/user/robo/images/lc-b.png"})

    def test_itHandlesUpperCaseLetters(self):
        fileList = ["UC-B.png",
                    "uC-C.png",
                    "UC-BOB.png"]
        result = parseFiles(self.fullPath, fileList)
        self.assertEquals(result, {"B": "/home/user/robo/images/UC-B.png"})


    # handling of punctuation leads to introduction of invalid glyph names
    # see bulubu
    def test_itHandlesPunctuation(self):
        fileList = ["punct-ampersand.png",
                    "punct-bulubu.png"]
        result = parseFiles(self.fullPath, fileList)
        self.assertEquals(result, {"ampersand": "/home/user/robo/images/punct-ampersand.png",
                                    "bulubu": "/home/user/robo/images/punct-bulubu.png" })


def main():
    unittest.main()

if __name__ == '__main__':
    main()