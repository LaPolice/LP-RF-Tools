# menuTitle: Simple Versioning
# shortCut: command+alt+shift+s
# script version: 1.3
# description: Simple versioning system supporting the La Police type development process.
# developer: La Police (David Hodgetts), Ryan Bugden
# developer URL: www.lapolice.ch
# tags: versioning, workflow
# bug report, feature request: https://github.com/LaPolice (file an issue)
# software compatibility:
# RoboFont 1.x: working (1.8.6)
# RoboFont 3.x: not tested
# RoboFont 4.x: working (4.5)



from collections import namedtuple
import os, re, time, codecs
from mojo.UI import Message, CurrentFontWindow
import ezui



def explodePath(path):
    "returns (directory, filename, extension)"
    p, extension = os.path.splitext(path)
    directory, filename = os.path.split(p)
    return (directory, filename, extension)

Validation = namedtuple("Validation", ['success', 'errorMessage'])
FontState = namedtuple("FontState", ['fullPath', 'directory', 'basename', 'versionMinor'])

def successfulValidation():
    return Validation(success=True, errorMessage="")

def failedValidation(errorMessage):
    return Validation(success=False, errorMessage=errorMessage)

def extractVersionFromFilename(filename):
    m = re.match(r".+-[A-Z](\d{3})$", filename)
    return int(m.group(1)) if m else -1

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
        return failedValidation("There is no open font")
    else:
        return successfulValidation()

def validateFilenameFormat(font):
    if font.path is None:
        return failedValidation("Font file name 'None' is invalid.")

    _, filename, _ = explodePath(font.path)
    version = extractVersionFromPath(font.path)
    return successfulValidation() if version > 0 else failedValidation(f"Font file name '{filename}' is invalid.")

def validateVersionsSynchronized(font):
    filenameVersion = extractVersionFromPath(font.path)
    versionMinor = font.info.versionMinor
    return successfulValidation() if versionMinor is filenameVersion else failedValidation(f"File name version ({filenameVersion}) out of sync with info.versionMinor ({versionMinor})")

def validateNextFontDoesNotExist(font):
    directory, filename, extension = explodePath(font.path)
    baseFileName = removeVersionFromFilename(filename)
    nextVersion = font.info.versionMinor + 1
    nextFontPath = os.path.join(directory, "%s%03d%s" % (baseFileName, nextVersion, extension))
    return successfulValidation() if not os.path.exists(nextFontPath) else failedValidation(f"The next font already exists: {nextFontPath}")

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
    logFileName = f"{fontState.basename[:-1]}changelog.md"
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
    newLogContent += "Version: 0.%03d  \n" % fontState.versionMinor
    newLogContent += "  \n"
    newLogContent += infoNoteContent + "  \n"
    newLogContent += u"\n---------------------------\n"

    logContent = newLogContent + logContent

    with codecs.open(logPath, 'w', 'utf-8') as f:
        f.write(logContent)

    Message(
        message="Operation Completed",
        informativeText=newLogContent
    )


def commitVersion(font, fontState, log=True):
    # increment version
    newVersion = fontState.versionMinor + 1
    font.info.versionMinor = newVersion
    # clear info.note
    infoNoteContent = font.info.note
    font.info.note = None
    # define newfilename and new path
    filename = "%s%03d.ufo" % (fontState.basename, newVersion)
    newPath = os.path.join(fontState.directory, filename)
    print ("Saving new font: %s" % newPath)
    font.save(newPath)
    font.close()
    font = OpenFont(newPath)
    if log:
        logToFile(fontState, infoNoteContent)


def commitInfoNote(infoNoteContent, font, fontState):
    if infoNoteContent == "":
        Message(
            message="Operation Aborted",
            informativeText="Info note is blank."
        )
    else:
        font.info.note = infoNoteContent
        print (f"Saving changes on font: {font.path}")
        oldFont = font.copy()
        # Ensure template glyph order and guidelines are in sync.
        oldFont.templateGlyphOrder = font.templateGlyphOrder
        oldFont.clearGuidelines()
        for guideline in font.guidelines: oldFont.appendGuideline(guideline=guideline)
        oldFont.save(font.path)
        commitVersion(font, fontState)
        
        
class SimpleVersioning(ezui.WindowController):

    def build(self, parent, font, fontState):
        self.font = font
        self.fontState = fontState
        content = """
        !§ Font Info Note
        [[_ _]]              @textEditor
        
        * HorizontalStack    @buttonStack
        > (Update Note)      @updateButton
        > (New Version)      @commitButton
        
        ---
        ===
        
        (Cancel)             @cancelButton
        """
        descriptionData = dict(
            textEditor=dict(
                height=200,
                width=300,
            ),
            buttonStack=dict(
                distribution="fillEqually"
            ),
            cancelButton = dict(
                keyEquivalent=chr(27)  # call button on esc keydown
            )
        )
        self.w = ezui.EZSheet(
            size="auto",
            content=content,
            descriptionData=descriptionData,
            controller=self,
            defaultButton="commitButton",
            parent=parent,
        )
        self.textEditor = self.w.getItem("textEditor")
        if self.font.info.note:
            self.textEditor.set(self.font.info.note)

    def started(self):
        self.w.open()
        self.textEditorCallback(self.textEditor)
        
    def cancelButtonCallback(self, sender):
        self.w.close()
        
    def commitButtonCallback(self, sender):
        note = self.textEditor.get()
        self.w.close()
        commitInfoNote(note, self.font, self.fontState)
        
    def updateButtonCallback(self, sender):
        self.font.info.note = self.textEditor.get()
        self.w.close()

    def textEditorCallback(self, sender):
        def enableButtons(enable=True):
            buttons = [self.w.getItem("commitButton"), self.w.getItem("updateButton")]
            for button in buttons:
                button.enable(enable)
        if sender.get():
            enableButtons(True)
        else:
            enableButtons(False)



# Run script
font = CurrentFont()
success, maybeFontState = getFontState(font)
if not success:
    Message(
        message="Script Validation Failed",
        informativeText="Fix and try again:\n" + maybeFontState
    )
else:
    parent = CurrentFontWindow().w
    SimpleVersioning(parent, font, maybeFontState)

    

