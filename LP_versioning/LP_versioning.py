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
    version = extractVersionFromFilename(filename)
    return successfullValidation() if version > 0 else failedValidation("font filename '%s' is invalid" % filename)



def getFontState(font):
    parseFontStateValidationFuncs = [validatePresenceOfFont, validateFilenameFormat]
    validationsResult = runValidationsOnValue(font, parseFontStateValidationFuncs)

    if not validationsResult.success:
        return (False, validationsResult.errorMessage)

    

