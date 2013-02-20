import sys, os

# add scripts dir to sys.path
scripts_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'scripts'))

sys.path.append(scripts_dir)

from addImagesToCurrentFont import parseFiles
import unittest



class TestParseDirectory(unittest.TestCase):

    fullPath = "/home/robo/images/"

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
        self.assertEquals(result, {"zero": "/home/robo/images/num-0.png"})
    
        
    # handling of punctuation can lead to introduction of invalid glyph names
    def test_itHandlesLowerCaseLetters(self):
        fileList = ["lc-b.png",
                    "lC-A.png",
                    "lc-invalidglyphname.png"]
        result = parseFiles(self.fullPath, fileList)
        self.assertEquals(result, {"b": "/home/robo/images/lc-b.png",
                                   "invalidglyphname": "/home/robo/images/lc-invalidglyphname.png"})

    # handling of punctuation can lead to introduction of invalid glyph names
    def test_itHandlesUpperCaseLetters(self):
        fileList = ["UC-B.png",
                    "uC-C.png",
                    "UC-INVALIDGLYPHNAME.png"]
        result = parseFiles(self.fullPath, fileList)
        self.assertEquals(result, {"B": "/home/robo/images/UC-B.png",
                                   "INVALIDGLYPHNAME": "/home/robo/images/UC-INVALIDGLYPHNAME.png"})


    # handling of punctuation can lead to introduction of invalid glyph names
    def test_itHandlesPunctuation(self):
        fileList = ["punct-ampersand.png",
                    "punct-bulubu.png"]
        result = parseFiles(self.fullPath, fileList)
        self.assertEquals(result, {"ampersand": "/home/robo/images/punct-ampersand.png",
                                    "bulubu": "/home/robo/images/punct-bulubu.png" })


def main():
    unittest.main()

if __name__ == '__main__':
    main()