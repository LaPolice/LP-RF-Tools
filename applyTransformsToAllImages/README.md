# LP_applyImageTransformToAll

this script has two possible behaviors depending on the available api (robofont version).

It will use the settable transform property if available (robofont >= Version 1.4b (built 1307152301)). This is preferable since it copies the transformation instead of applying it on top of the existing value. 

Otherwise, it will use the transform method to apply the transformation on the target transformation.

## usage

Step 1.

import some images (for instance using LP_addImagesToCurrentFont.py).
If you use LP_addImagesToCurrentFont go to step2

The script expects the images to be on a layer named "imported_images".
If needed you can change this value on line 3 of the script(replace "imported_images" by "name_of_your_layer")

Step 2.

select a glyph and use the Set Scale function to define the desired transformations.
apply Scale to your glyph image.

Step 3.

run the script with the transformed image as the current window.
It will apply/copy the transformations to all imported images. 
