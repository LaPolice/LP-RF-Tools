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
        try:
            glyph = font.getGlyph(glyphName)
        except:
            glyph = None
            
        if glyph != None:
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
            glyph.mark = (0,1, 0.2,1)
        else:
            glyph = font.newGlyph("%r" % c)
            glyph.mark = (1, 0, 0, 1)
            unhandledCharacters.append(c)
    
    return unhandledCharacters


def textCharsetToFont(font):
    charset = extractCharset(window.textEditor.get())
    unhandledCharacters = applyCharsetToFont(font, charset)
    print "-------------"
    print "total unique characters", len(charset)
    if len(unhandledCharacters) > 0:
        print "characters marked in red are not in the latin-1 set, you must rename them appropriately"
        print unhandledCharacters
    
def onSubmit(sender):
    currentFont = CurrentFont()
    if currentFont is not None:
        textCharsetToFont(currentFont)
    else:
        print "there is no current font, operation aborted" 
    

window = vanilla.Window((400, 400),"paste text into box and press submit", minSize=(100, 100))
window.textEditor = vanilla.TextEditor(posSize=(0, 0, 400, 300))
window.submitButton = vanilla.SquareButton(posSize=(0, 350, 100, 50), title="submit", callback=onSubmit)


window.open()
