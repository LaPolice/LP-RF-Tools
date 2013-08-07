# LP_charsetFromText.py

extracts the set of characters in use in a text, and marks all occurrences in a new font page.
Also returns a count of the set.

The script marks in green glyphs who belong to the latin-1 default charset. Glyphs outside of Latin-1 will be marked in red, and named with their unicode value. It is up to the user to rename them appropriately.

## usage

step 1.
open a new font

step 2.
run the script and paste the text to parse in the text area. The text is expected to be utf-8 encoded.

step 3.
press submit
