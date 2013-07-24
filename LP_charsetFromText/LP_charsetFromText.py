import vanilla
import mojo

from sets import Set

def extractCharset(text):
    charset = Set()
    for char in text:
        charset.add(char)

    filteredCharset = filter(lambda c: c != u'\n' and c != u' ', charset)
    print filteredCharset
    return filteredCharset

def applyCharsetToCurrentFont(charset):

    for c in charset:
        g = CurrentFont().newGlyph(c)
        g.unicode = ord(c)


def textCharsetToCurrentFont():
    charset = extractCharset(window.textEditor.get())
    applyCharsetToCurrentFont(charset)
    
def onSubmit(sender):
    textCharsetToCurrentFont()
    

window = vanilla.Window((400, 400),"paste text into box and press submit", minSize=(100, 100))
window.textEditor = vanilla.TextEditor(posSize=(0, 0, 400, 300))
window.submitButton = vanilla.SquareButton(posSize=(0, 350, 100, 50), title="submit", callback=onSubmit)


window.open()
