
import os, re, sys, operator
from os.path import join, isfile

# list of custom glyph names
# these glyphs will be added to the current font if images exist for them
# modify this list to support your own custom glyph names
customGlyphs = ["Dswash", "Mswash", "Pfswash"]

# handle UC lc and num
def extractKeyFromCategorizedBaseNames(basename):
    key = None
    key = extractKeyFromNumber(basename) or extractKeyFromLowerCase(basename) or extractKeyFromUpperCase(basename) 
    return key 

# handle all except lc UC and num
def extractKeyFromUnCategorizedBaseNames(basename):

    regex = re.compile("^([a-zA-Z]{2,})$")

    return extractKeyFromBaseNameAndRegex(basename, regex)


def extractKeyFromBaseNameAndRegex(basename, regex):
    key = None
    
    m = regex.match(basename)

    if m and len(m.groups()) > 0:
        key = reduce(operator.add, m.groups())


    return key

def extractKeyFromNumber(basename):
    key = None
    num_re = re.compile("^num-([a-z]{3,})$", re.IGNORECASE)
    numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    m = num_re.match(basename)

    if m and m.group(1) in numbers:
        key = m.group(1)

    return key



def extractKeyFromLowerCase(basename):
    
    singleLetterRegex = re.compile("^lc-([a-z]{1,2})$")
    complexLetterRegex = re.compile("^lc-([a-z])-([a-z]{1,})$")

    key = extractKeyFromBaseNameAndRegex(basename, singleLetterRegex)

    if key:
        return key
    else:
        return extractKeyFromBaseNameAndRegex(basename, complexLetterRegex)


def extractKeyFromUpperCase(basename):
    
    singleLetterRegex = re.compile("^UC-([A-Z]{1,2})$")
    complexLetterRegex = re.compile("^UC-([A-Z])-([a-z]{1,})$")

    key = extractKeyFromBaseNameAndRegex(basename, singleLetterRegex)

    if key:
        return key
    else:
        return extractKeyFromBaseNameAndRegex(basename, complexLetterRegex)


def extractKeyFromPunctuation(basename):
    
    regex = re.compile("^punct-([a-z]{2,})$")

    return extractKeyFromBaseNameAndRegex(basename, regex)

    
    


# parseFiles:
# given a list of files (fullpath string representation)
# return a dictionary where key is glyph name and value is full path to image
# for all valid images in listing
def parseFiles(pathToDir, fileList):

    result = {}


    # convert file names to (basename, extension)
    # TODO extract
    # TODO use dictionary or named tupple
    fileInfos = map (lambda fileName: ( os.path.splitext(os.path.basename(fileName))[0], 
                                        os.path.splitext(os.path.basename(fileName))[1][1:]),
                        fileList)


    valid_extensions = ['jpg', 'png', 'tif']

    invalidExtensionsRemoved = filter(lambda (_, extension): extension.lower() in valid_extensions, fileInfos)

    for basename, extension in invalidExtensionsRemoved:
        key = extractKeyFromCategorizedBaseNames(basename)
        isCustom = False

        if key == None:
            key = extractKeyFromUnCategorizedBaseNames(basename)
            if key: 
                isCustom = True

        fullFileName = join(pathToDir, basename) + '.' + extension
        if key:
            result[key] = fullFileName
        else:
            print "can't parse key for", fullFileName
    

    return result



def addImages(currentFont, dictOfImages):
    for glyphName, imagePath in dictOfImages.items():
        try:
            glyph = currentFont.getGlyph(glyphName)
        except:
            if glyphName in customGlyphs:
                print "creating new glyph %s" % glyphName
                glyph = currentFont.newGlyph(glyphName)
            else:
                print "invalid glyph name -> %s for path %s" % (glyphName, imagePath)
                continue

        # add image on layer "imported_images"

        glyph = glyph.getLayer("imported_images")
        glyph.addImage(imagePath)

        if glyph.image:
            print "image load succesful for glyph %s" % glyphName 
        else:
            print "image load failed for glyph %s and path %s" % (glyphName, imagePath)

def main():
    currentFont = CurrentFont()
    if currentFont == None:
        print "no font is open, aborting"
        return

    folder_path = getFolder()
    if folder_path:
        pathToDir = folder_path[0]
        files = [ f for f in os.listdir(pathToDir) if isfile(join(pathToDir,f)) and f[0] != '.']
        dictOfImages = parseFiles(pathToDir, files)
        addImages(currentFont, dictOfImages)

        print "all done"
    else:
        print "operation canceled"


# scripts launch point

runMain = True

try:
    import mojo    
    from vanilla.dialogs import getFolder
    
except:
    print "not running in context of robofont"
    runMain = False

if runMain:
    main()



