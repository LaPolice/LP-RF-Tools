Robofont scripts
----------------

addImagesToGlyphs
-----------------

takes a folder of bitmaps and loads them in their associated glyph window

image names are expected to conform to the following pattern

fileName, glyphName
-------------------
lc-a, a,
lc-ae, ae
lc-a-acute, aacute
UC-B, B
num-two, two
punct-ampersand, ampersand
punct-comma, comma

in other words "lc-a.tif" will be loaded in glyph "a"



applyImageTransformToAll
------------------------
applies the matrix transform of the current glyph image to all images found in the current font 

