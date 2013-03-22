
import os, re, sys, operator
from os.path import join, isfile


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
    
    


# parseFiles:
# given a list of files (fullpath string representation)
# return a dictionary where key is glyph name and value is full path to image
# for all valid images in listing
def parseFiles(pathToDir, fileList):

    categorizedKeys = {} # lc, UC and num

    unCategorizedKeys = {} # everything else


    # convert file names to tuple -> (basename, extension, fullFileName)
    # TODO use dictionary or named tupple
    fileInfos = map (lambda fileName: ( os.path.splitext(os.path.basename(fileName))[0], 
                                        os.path.splitext(os.path.basename(fileName))[1][1:]),
                        fileList)


    valid_extensions = ['jpg', 'png', 'tif']

    invalidExtensionsRemoved = filter(lambda (_, extension): extension.lower() in valid_extensions, fileInfos)

    for basename, extension in invalidExtensionsRemoved:
        fullFileName = join(pathToDir, basename) + '.' + extension
        key = extractKeyFromCategorizedBaseNames(basename)
        
        if key:
            categorizedKeys[key] = fullFileName
        else:
            key = extractKeyFromUnCategorizedBaseNames(basename)

            if key:
                unCategorizedKeys[key] = fullFileName
            else:
                print "can't parse key for", fullFileName
    

    return categorizedKeys, unCategorizedKeys


def warnOnGlyphCreation(newGlyphNames):
    print "--------------------------------"
    print "%i glyphs have been created" % len(newGlyphNames)
    print "new glyphs:"
    print "-----------"
    for name in newGlyphNames:
        print name

def addImageToGlyph(imagePath, glyph):
    # add image on layer "imported_images"

    glyph = glyph.getLayer("imported_images")
    glyph.addImage(imagePath)

    if glyph.image:
        print "image load succesful for glyph %s" % glyph.name 
    else:
        print "image load failed for glyph %s and path %s" % (glyph.name, imagePath)


def addImages(currentFont, tupleOfDicts):
    categorizedKeys, unCategorizedKeys = tupleOfDicts

    newGlyphNames = []

    for glyphName, imagePath in categorizedKeys.items():
        try:
            glyph = currentFont.getGlyph(glyphName)
        except:
            print "invalid glyph name -> %s for path %s" % (glyphName, imagePath)
            continue
        addImageToGlyph(imagePath, glyph)

    for glyphName, imagePath in unCategorizedKeys.items():
        try:
            glyph = currentFont.getGlyph(glyphName)
        except:     
            newGlyphNames.append(glyphName)
            glyph = currentFont.newGlyph(glyphName)
        addImageToGlyph(imagePath, glyph)

    if len(newGlyphNames) > 0:
        warnOnGlyphCreation(newGlyphNames)


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



