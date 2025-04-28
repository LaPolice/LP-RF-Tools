# Add images to current font

Takes a folder of bitmaps (jpg, tif or png) and loads them in their associated glyph window.

The script operates on the current font. On execution, a folder requester is opened to allow the user to point to the location of the images to be imported.

The image files should be named as follows:

Lower case letters are prefixed with "lc-".
Upper case letters are prefixed with "UC-".
digits (0-9) are prefixed with "num-".
Punctuation and special characters take no prefix.
In other words, a file named "lc-a.tif" will be loaded in glyph "a".

<table>
    <tr>
        <th>filename</th>
        <th>glyphname</th>
    </tr>
    <tr>
        <td>lc-a</td>
        <td>a</td>
    </tr>
    <tr>
        <td>lc-ae</td>
        <td>ae</td>
    </tr>
    <tr>
        <td>lc-a-acute</td>
        <td>aacute</td>
    </tr>
    <tr>
        <td>UC-B</td>
        <td>B</td>
    </tr>
    <tr>
        <td>num-two</td>
        <td>two</td>
    </tr>
    <tr>
        <td>comma</td>
        <td>comma</td>
    </tr>
    <tr>
        <td>Dswash</td>
        <td>Dswash</td>
    </tr>
</table>
 

The images are imported on a layer named "imported_images".
