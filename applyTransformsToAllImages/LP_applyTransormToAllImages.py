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



