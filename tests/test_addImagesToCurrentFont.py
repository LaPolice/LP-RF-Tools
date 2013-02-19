import sys, os

# add scripts dir to sys.path
scripts_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'scripts'))

sys.path.append(scripts_dir)

from addImagesToCurrentFont import parseFileList
import unittest



# Here's our "unit tests".
class TestParseDirectory(unittest.TestCase):

    def test_itReturnsADictionary(self):
        self.failUnless( isinstance(parseFileList([]), dict))


    def test_itFiltersInvalidFileExtensions(self):
    	fileList = ["/home/user/robo/images/lc-b.txt",
    				"/home/user/robo/images/lc-a.doc",
    				"/home/user/robo/images/lc-a.ai"]
    	result = parseFileList(fileList)
    	self.assertEquals(len(result), 0)


    def test_itHandlesNumbers(self):
        fileList = ["/home/user/robo/images/num-0.png",
                    "/home/user/robo/images/num-10.png"]
        result = parseFileList(fileList)
        self.assertEquals(result, {"zero": "/home/user/robo/images/num-0.png"})
        

    def test_itHandlesLowerCaseLetters(self):
        fileList = ["/home/user/robo/images/lc-b.png",
                    "/home/user/robo/images/lC-A.png",
                    "/home/user/robo/images/lc-bob.png"]
        result = parseFileList(fileList)
        self.assertEquals(result, {"b": "/home/user/robo/images/lc-b.png"})

    def test_itHandlesUpperCaseLetters(self):
        fileList = ["/home/user/robo/images/UC-B.png",
                    "/home/user/robo/images/uC-C.png",
                    "/home/user/robo/images/UC-BOB.png"]
        result = parseFileList(fileList)
        self.assertEquals(result, {"B": "/home/user/robo/images/UC-B.png"})


    # handling of punctuation leads to introduction of invalid glyph names
    # see bulubu
    def test_itHandlesPunctuation(self):
        fileList = ["/home/user/robo/images/punct-ampersand.png",
                    "/home/user/robo/images/punct-bulubu.png"]
        result = parseFileList(fileList)
        self.assertEquals(result, {"ampersand": "/home/user/robo/images/punct-ampersand.png",
                                    "bulubu": "/home/user/robo/images/punct-bulubu.png" })


def main():
    unittest.main()

if __name__ == '__main__':
    main()