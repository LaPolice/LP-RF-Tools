# menuTitle: Apply transforms to all images
# description: Applies transformations to images. Consult the readme file, this script has two possible behaviors depending on the available api (robofont version).
# script version: 1.0
# developer: La Police (David Hodgetts)
# developer URL: www.lapolice.ch
# tags: 
# bug report, feature request: https://github.com/LaPolice (file an issue)
# software compatibility:
# RoboFont 1.x: working (1.8.6)
# RoboFont 3.x: not tested
# RoboFont 4.x: not working (4.5)

import mojo

TARGET_LAYER_NAME = "imported_images"

def applyImageTransFormToAllImagesClassic(sourceGlyphWithTargetLayer):
    """
    applies sourceGlyphWithTargetLayer' image transformMatrix on all other images 
    of the same layer (layer of sourceGlyphWithTargetLayer)
    warning this function is not idempotent
    """

    sourceImageTransformMatrix = sourceGlyphWithTargetLayer.image.transformMatrix
    targetLayer = sourceGlyphWithTargetLayer.layerName

    for glyph in CurrentFont():
        destinationGlyph = glyph.getLayer(targetLayer)
        if destinationGlyph == sourceGlyphWithTargetLayer:
            continue
        if destinationGlyph.image:
            destinationGlyph.image.transform(sourceImageTransformMatrix)
            print "applying (not copying) matrix from glyph %s to glyph %s" % (sourceGlyphWithTargetLayer, destinationGlyph)
            print "destinationTransformMatrix", destinationGlyph.image.transformMatrix

    print "all done"

def applyImageTransFormToAllImages(sourceGlyphWithTargetLayer):
    """
    copies sourceGlyphWithTargetLayer's image transformation on all other images 
    of the same layer (layer of sourceGlyphWithTargetLayer)
    """

    sourceImageTransformation = sourceGlyphWithTargetLayer.image.transformation
    targetLayer = sourceGlyphWithTargetLayer.layerName

    for glyph in CurrentFont():
        destinationGlyph = glyph.getLayer(targetLayer)
        if destinationGlyph == sourceGlyphWithTargetLayer:
            continue
        if destinationGlyph.image:
            destinationGlyph.image.transformation = sourceImageTransformation
            print "copying matrix from glyph %s to glyph %s" % (sourceGlyphWithTargetLayer, destinationGlyph)
            print "destination transformation", destinationGlyph.image.transformation

    print "all done"

def imageUsesTransformMatrix(image):

    result = True
    try:
        image.transformMatrix
    except AttributeError:
        result = False

    return result



def doMain(sourceGlyph):
    sourceGlyphWithTargetLayer = sourceGlyph.getLayer(TARGET_LAYER_NAME)

    # check presence of image
    if (not sourceGlyphWithTargetLayer.image):
        print "no image on current glyph", sourceGlyphWithTargetLayer
        return

    if imageUsesTransformMatrix(sourceGlyphWithTargetLayer.image):
        # uses image.transformMatrix (old school)
        applyImageTransFormToAllImagesClassic(sourceGlyphWithTargetLayer)
    else:
        # uses new api -> image.transformation
        applyImageTransFormToAllImages(sourceGlyphWithTargetLayer)



# main

sourceGlyph = CurrentGlyph()

if sourceGlyph == None:
    print "no current glyph accessible, script aborting"
else:
    doMain(sourceGlyph)



