import vanilla
import mojo

from sets import Set

def extractCharset(text):
    charset = Set()
    for char in text:
        charset.add(char)

    filteredCharset = filter(lambda c: c != u'\n' and c != u' ', charset)
    return filteredCharset

def buildDictFromUnicodeToGlyphname():
    "HACK: builds a dict from unicode to glyphnames"
    latin_1_set = mojo.UI.getCharacterSets()['Latin-1']
    font = NewFont()
    result = {}
    for glyphName in latin_1_set:
        glyph = font.getGlyph(glyphName)
        result[glyph.unicode] = glyphName
    font.close(False)
    return result

def applyCharsetToFont(font, charset):
    unhandledCharacters = []

    unicodeGlyphNamesDict = buildDictFromUnicodeToGlyphname()

    for c in charset:
        c_int = ord(c)
        if c_int in unicodeGlyphNamesDict:
            glyph = font.getGlyph(unicodeGlyphNamesDict[c_int])
            glyph.mark = (0,0,1,1)
        else:
            unhandledCharacters.append(c)
    
    return unhandledCharacters


def textCharsetToCurrentFont():
    charset = extractCharset(window.textEditor.get())
    unhandledCharacters = applyCharsetToFont(CurrentFont(), charset)
    print "total unique characters", len(charset)
    if len(unhandledCharacters) > 0:
        print "this script only handles character defined in the default Latin-1 charset:"
        print "following characters will have to be added by hand"
        print unhandledCharacters
    
def onSubmit(sender):
    textCharsetToCurrentFont()
    

window = vanilla.Window((400, 400),"paste text into box and press submit", minSize=(100, 100))
window.textEditor = vanilla.TextEditor(posSize=(0, 0, 400, 300))
window.submitButton = vanilla.SquareButton(posSize=(0, 350, 100, 50), title="submit", callback=onSubmit)


window.open()
