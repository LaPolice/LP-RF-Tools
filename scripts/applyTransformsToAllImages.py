import mojo

sourceGlyph = CurrentGlyph()

imageTransformMatrix = sourceGlyph.image.transformMatrix

print imageTransformMatrix

for g in CurrentFont():
   if g == sourceGlyph:
       continue
   if g.image:
       g.image.transform(imageTransformMatrix)
