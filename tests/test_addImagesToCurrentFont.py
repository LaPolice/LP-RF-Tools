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
    				"/home/user/robo/images/lc-a.jpg",
    				"/home/user/robo/images/lc-a.JpG"]
    	result = parseFileList(fileList)
    	print result
    	self.failUnless(len(result) == 1)






def main():
    unittest.main()

if __name__ == '__main__':
    main()