from collections import namedtuple
import os, re, time, codecs

def explodePath(path):
    "returns (directory, filename, extension)"
    p, extension = os.path.splitext(path)
    directory, filename = os.path.split(p)
    return (directory, filename, extension)

Validation = namedtuple("Validation", ['success', 'errorMessage'])
FontState = namedtuple("FontState", ['fullPath', 'directory', 'basename', 'versionMinor'])

def successfullValidation():
    return Validation(success=True, errorMessage="")

def failedValidation(errorMessage):
    return Validation(success=False, errorMessage=errorMessage)

def extractVersionFromFilename(filename):
    regex = re.compile(".+-[A-Z](\d{3})$")
    m = regex.match(filename)
    return int(m.groups()[0]) if m is not None else -1

def extractVersionFromPath(path):
     _, filename, _ = explodePath(path)
     return extractVersionFromFilename(filename)

def removeVersionFromFilename(filename):
    """returns 'file-B' for 'file-B001'"""
    return filename[:-3]

def runValidationsOnValue(value, validations):
    operation = None
    for f in validations:
        operation = f(value)
        if not operation.success:
            return operation

    return operation

def validatePresenceOfFont(font):
    if font is None:
        return failedValidation("there is no open font")
    else:
        return successfullValidation()

def validateFilenameFormat(font):
    if font.path is None:
        return failedValidation("font filename 'None' is invalid")

    _, filename, _ = explodePath(font.path)
    version = extractVersionFromPath(font.path)
    return successfullValidation() if version > 0 else failedValidation("font filename '%s' is invalid" % filename)

def validateVersionsSynchronized(font):
    filenameVersion = extractVersionFromPath(font.path)
    versionMinor = font.info.versionMinor

    return successfullValidation() if versionMinor is filenameVersion else failedValidation("filename version(%i) out of sync with info.versionMinor(%r)" % (filenameVersion, versionMinor))

def validateNextFontDoesNotExist(font):
    directory, filename, extension = explodePath(font.path)
    baseFileName = removeVersionFromFilename(filename)
    nextVersion = font.info.versionMinor + 1
    nextFontPath = os.path.join(directory, "%s%03d%s" % (baseFileName, nextVersion, extension))

    return successfullValidation() if not os.path.exists(nextFontPath) else failedValidation("the next font already exists %s" % nextFontPath)

def getFontState(font):
    parseFontStateValidationFuncs = [validatePresenceOfFont, 
                                     validateFilenameFormat,
                                     validateVersionsSynchronized,
                                     validateNextFontDoesNotExist]
    validationsResult = runValidationsOnValue(font, parseFontStateValidationFuncs)

    if validationsResult.success:
        directory, filename, _ = explodePath(font.path)
        basename = removeVersionFromFilename(filename)
        versionMinor = font.info.versionMinor
        return (True, FontState(fullPath=font.path,
                                directory=directory, 
                                basename=basename, 
                                versionMinor=versionMinor))
    else:
        return (False, validationsResult.errorMessage)

def ensureDirectoryExists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def logToFile(fontState, infoNoteContent):
    directory, filename, extension = explodePath(fontState.fullPath)
    logFileName = "%schangelog.md" % fontState.basename[:-1]
    changelogsFolderPath = os.path.join(directory, "changelogs")
    ensureDirectoryExists(changelogsFolderPath)
    logPath = os.path.join(changelogsFolderPath, logFileName)
    
    if (os.path.exists(logPath)):
        with codecs.open(logPath, 'r', 'utf-8') as f:
            logContent = f.read()
    else:
        logContent = u""
    
    newLogContent = time.strftime("### %d.%m.%Y (%H:%M)  \n")
    newLogContent += "**%s%s**  \n" % (filename, extension)
    newLogContent += "version: 0.%03d  \n" % fontState.versionMinor
    newLogContent += "  \n"
    newLogContent += infoNoteContent + "  \n"
    newLogContent += u"\n---------------------------\n"

    logContent = newLogContent + logContent

    with codecs.open(logPath, 'w', 'utf-8') as f:
        f.write(logContent)

    message("operation completed\n" + newLogContent)


def commitVersion(font, fontState, log=True):
    # increment version
    newVersion = fontState.versionMinor + 1
    font.info.versionMinor = newVersion
    # clear info.note
    infoNoteContent = font.info.note
    font.info.note = None
    #define newfilename and new path
    filename = "%s%03d.ufo" % (fontState.basename, newVersion)
    newPath = os.path.join(fontState.directory, filename)
    print ("saving new font: %s" % newPath)
    font.save(newPath)
    if log:
        logToFile(fontState, infoNoteContent)


def commitInfoNote(infoNoteContent, font, fontState):
    if infoNoteContent == "":
        message("info note is blank, operation aborted")
    else:
        font.info.note = infoNoteContent
        print ("saving changes on font: %s" % font.path)
        font.copy().save(font.path)
        commitVersion(font, fontState)


def userChecksInfoNote(font, fontState):
    window = Window((400, 400),"edit info.note", minSize=(100, 100))
    window.textEditor = TextEditor(posSize=(0, 0, 400, 300))
    noteContent = font.info.note or ""
    window.textEditor.set(noteContent)
    def handleCommit(s):
        editorContent = window.textEditor.get()
        window.close()
        commitInfoNote(editorContent, font, fontState)
    window.updateNoteButton = SquareButton(posSize=(0, 350, 100, 50), title="commit", callback=handleCommit)
    window.cancelButton = SquareButton(posSize=(110, 350, 130, 50), title="cancel operation", callback=lambda x: window.close())
    window.open()




def main():
    font = CurrentFont()
    success, maybeFontState = getFontState(font)

    if not success:
        message("script validation failed(fix and try again):\n" + maybeFontState)
    else:
        userChecksInfoNote(font, maybeFontState)

# script launch point

runMain = True

try:
    import mojo    
    from vanilla.dialogs import message
    from vanilla import Window, SquareButton, TextEditor
except:
    print("not running in context of robofont")
    runMain = False

if runMain:
    main()
    

