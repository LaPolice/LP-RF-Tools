import vanilla
import mojo
from mojo.UI import getCharacterSets, getDefaultCharacterSet
from fontTools import agl
from sets import Set

def extractCharset(text):
    charset = Set()
    for char in text:
        charset.add(char)

    removeSet = Set([u'\n', u'\r', u'\r\n', u' ', u"\u00A0"])

    filteredCharset = charset - removeSet
    return filteredCharset


def applyCharsetToFont(font, charset):
    notInFontGlyphNames = []

    for c in charset: 
        gname = agl.UV2AGL[ord(c)]
        
        try:
            glyph = font.getGlyph(gname)
            glyph.mark = (0,1, 0.2,1)
        except:
            glyph = font.newGlyph(gname)
            glyph.mark = (1, 0, 0, 1)
            notInFontGlyphNames.append(gname)
    
    return notInFontGlyphNames


def textCharsetToFont(font):
    charset = extractCharset(window.textEditor.get())
    notInFontGlyphNames = applyCharsetToFont(font, charset)
    print "-------------"
    print "total unique characters", len(charset)
    if len(notInFontGlyphNames) > 0:
        print "characters marked in red are not in the current font charset"
        print notInFontGlyphNames
    
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
