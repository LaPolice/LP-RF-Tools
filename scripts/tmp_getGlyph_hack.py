import mojo
from mojo.compile import *


try:
    print CurrentFont().getGlyph("pipo")
except RoboFontError:
    print "invalid glyph"