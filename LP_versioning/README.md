# LP_versioning

simple versioning system supporting _laPolice_ type development process.
The script validates the current state of the font. If it is valid, it will save the file as an incremented verison and will update a .changelog file with the new changes.

## validations

### 1. font presence

checks if a font is open in current font

### 2. file name format

a valid format is derived from the following formula:
			fontName + '-' + upperCaseLetter + versionMinor + '.ufo'

_fontName_ can be any non blank word
_upperCaseLetter_ is any one upperCase letter
_versionMinor_ is a 3 digit version number (0 padded)

valid formats

			"fontName-A001.ufo", "jung-regular-Z001.ufo"

invalid formats

			"A001.ufo", "jung-regular-a001.ufo", "jung-regular-A1.ufo"
			
### 3. versions are in sync

check that the filename's version equals the value found in info.versionMinor

### 4. info.note not blank

check that info.note is not blank (info.note will be used to update the changelog file)

### 5. make sure there is no file corresponding to the next version

for a font with path "/foo/fontName-A001.ufo", ensure "/foo/fontName-A002.ufo" does not already exist
