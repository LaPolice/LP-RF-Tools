from collections import namedtuple
import os, re



def explodePath(path):
    "returns (directory, filename, extension)"
    p, extension = os.path.splitext(path)
    directory, filename = os.path.split(p)
    return (directory, filename, extension)

Validation = namedtuple("Validation", ['success', 'errorMessage'])

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

    return successfullValidation() if versionMinor is filenameVersion else failedValidation("filename version(%i) out of sync with info.versionMinor(%i)" % (filenameVersion, versionMinor))

def validateNoteNotBlank(font):
    return successfullValidation() if font.info.note else failedValidation("font info note is blank, please write a changelogMessage")

def getFontState(font):
    parseFontStateValidationFuncs = [validatePresenceOfFont, 
                                     validateFilenameFormat,
                                     validateVersionsSynchronized,
                                     validateNoteNotBlank]
    validationsResult = runValidationsOnValue(font, parseFontStateValidationFuncs)

    if not validationsResult.success:
        return (False, validationsResult.errorMessage)

    

