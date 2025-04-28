# LP_versioning

Simple versioning system supporting the _La Police_ type development process.

## process

### 1. validations
Validate the font state. if font state is invalid terminate with an error message.

### 2. user validation of info.note
User is asked to check and edit info.note. The script is terminated if she presses cancels or info.note is an empty string.  
The content of info.note should describe the changes pertaining to the current version of the font.

### 3. "commit" current version
The current version is saved (and ideally should never be saved again)

### 4. create next version
A new version of the font is saved and made available for further development. The new font has its file name and version minor field incremented and its info.note field cleared.

### 5. update changelog
A changelog.md file is updated with a version header and the content of info.note. This file resides in the same folder as the font in a folder named `changelogs`. It will be created if necessary.

## validations

### 1. font presence

checks if a font is open in current font

### 2. file name format

a valid format is derived from the following formula:
			fontName + '-' + upperCaseLetter + versionMinor + '.ufo'

_fontName_ can be any non blank word
_upperCaseLetter_ is any one upperCase letter
_versionMinor_ is a 3 digit version number (0 padded)

valid formats:

			"fontName-A001.ufo", "jung-regular-Z001.ufo"

invalid formats:

			"A001.ufo", "jung-regular-a001.ufo", "jung-regular-A1.ufo"


note that this system uses a 3 character padded version number. The script does not currently handle more than 999 versions, and will not warn the user in case of a loop over.
			
### 3. versions are in sync

check that the filename's version equals the value found in info.versionMinor


### 4. make sure there is no file corresponding to the next version

for a font with path "/foo/fontName-A001.ufo", ensure "/foo/fontName-A002.ufo" does not already exist
