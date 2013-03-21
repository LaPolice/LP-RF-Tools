

addImagesToGlyphs
=================

takes a folder of bitmaps (jpg, tif or png) and loads them in their associated glyph window

the script operates on the current font. On execution, a folder requester is presented to allow the user to point to the location of the images to be imported.

Each filename should correspond to a standard robofont glyphName.
The following pattern is expected:

fileName -> glyphName
-------------------
lc-a -> a
lc-ae -> ae
lc-a-acute -> aacute
UC-B -> B
num-two -> two
punct-ampersand -> ampersand
punct-comma -> comma
punct-Dswash -> Dswash

in other words "lc-a.tif" will be loaded in glyph "a"

the script expects the glyphNames to be identical to the standard robofont glyphNames.

To import custom glyphs that are not in this set, you must edit the script and add your own glyphNames to the "customGlyphs" list (top of script). The script will create these custom glyphs providing they have an associated image.



applyImageTransformToAll
========================

applies the matrix transform of the current glyph image to all images found in the current font 

