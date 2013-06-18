# applyImageTransformToAll

applies the matrix transform of the current glyph image to all images found in the current font 
works on layer "imported_images".

once the images have been imported with addImagesToCurrentFont.py (works with manually imported images as well), select a glyph and use the Set Scale function to define the transformations you want.

apply Scale to your glyph and then run the script, which will apply the same transformations to all imported images. 
beware, the script only works with the initial Set Scale!

TODO: make the script copy the matrix not apply it. This would allow more predictable behavior