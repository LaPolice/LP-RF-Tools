
import os, re

try:
	import mojo
except:
	print "not running in context of robofont"


def extractKeyFromBaseName(basename):
	key = None
	key = extractKeyFromNumber(basename) or extractKeyFromLowerCase(basename) 
	key = key or extractKeyFromUpperCase(basename) or extractKeyFromPunctuation(basename)
	return key

def extractKeyFromNumber(basename):
	key = None
	num_re = re.compile("^num-(\d)$", re.IGNORECASE)
	numbers = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
				"5": "five", "6": "six", "7": "seven", "8": "eight", "9":"nine"}

	m = num_re.match(basename)

	if m:
		key = numbers[m.group(1)]

	return key

def extractKeyFromBaseNameAndRegex(basename, regex):
	key = None
	
	m = regex.match(basename)

	if m:
		key = m.group(1)

	return key

def extractKeyFromLowerCase(basename):
	
	regex = re.compile("^lc-([a-z])$")

	return extractKeyFromBaseNameAndRegex(basename, regex)

def extractKeyFromUpperCase(basename):
	
	regex = re.compile("^UC-([A-Z])$")

	return extractKeyFromBaseNameAndRegex(basename, regex)


def extractKeyFromPunctuation(basename):
	
	regex = re.compile("^punct-([a-z]{2,})$")

	return extractKeyFromBaseNameAndRegex(basename, regex)

	
	


# parseFileList:
# given a list of files (fullpath string representation)
# return a dictionary where key is glyph name and value is full path to image
# for all valid images in listing
def parseFileList(fileList):

	result = {}


	# convert file of fullpath string to list of (fullPath, basename, extension)
	# TODO extract
	# TODO use dictionary or named tupple
	fileInfos = map (lambda fullPath: (fullPath, 
										 os.path.splitext(os.path.basename(fullPath))[0], 
										 os.path.splitext(os.path.basename(fullPath))[1][1:]),
						fileList)


	valid_extensions = ['jpg', 'png', 'tif']

	invalidExtensionsRemoved = filter(lambda (_, __, extension): extension.lower() in valid_extensions, fileInfos)

	for fullpath, basename, _ in invalidExtensionsRemoved:
		key = extractKeyFromBaseName(basename)
		if key:
			result[key] = fullpath
	


	return result




