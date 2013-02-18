
import os

try:
	import mojo
except:
	print "not running in context of robofont"


valid_extensions = ['jpg', 'png', 'tif']


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



	invalidExtensionsRemoved = filter(lambda (_, __, extension): extension.lower() in valid_extensions, fileInfos)

	for fullPath, baseName, extension in invalidExtensionsRemoved:
		result[baseName] = fullPath


	return result




