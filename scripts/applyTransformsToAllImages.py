import mojo

TARGET_LAYER_NAME = "imported_images"

def applyImageTransFormToAllImages(sourceGlyph, targetLayer):


    sourceGlyphWithTargetLayer = sourceGlyph.getLayer(targetLayer)

    if (sourceGlyphWithTargetLayer.image):
        sourceImageTransformMatrix = sourceGlyphWithTargetLayer.image.transformMatrix
        print "sourceImageTransformMatrix",  sourceImageTransformMatrix
    else:
        print "no image on current glyph", sourceGlyphWithTargetLayer
        return


    for glyph in CurrentFont():

        destinationGlyph = glyph.getLayer(targetLayer)
        if destinationGlyph == sourceGlyphWithTargetLayer:
            continue
        if destinationGlyph.image:
            destinationGlyph.image.transform(sourceImageTransformMatrix)
            print "applying (not copying) matrix from glyph %s to glyph %s" % (sourceGlyphWithTargetLayer, destinationGlyph)
            print "destinationTransformMatrix", destinationGlyph.image.transformMatrix

    print "all done"


# main

sourceGlyph = CurrentGlyph()

if sourceGlyph == None:
    print "no current glyph accessible, script aborting"
else:
    applyImageTransFormToAllImages(sourceGlyph, TARGET_LAYER_NAME)



