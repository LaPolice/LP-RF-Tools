# menuTitle: Update-font-info-note
# script version: 1.0
# description: Allows quick access and editing of the current font's info.note content, to pair with Simple versioning.
# developer: La Police (David Hodgetts)
# developer URL: www.lapolice.ch
# tags: 
# bug report, feature request: https://github.com/LaPolice (file an issue)
# software compatibility:
# RoboFont 1.x: working (1.8.6)
# RoboFont 3.x: not tested
# RoboFont 4.x: working (4.5)

from vanilla import Window, SquareButton, TextEditor
import vanilla
import mojo

def onSubmit(sender): 
    CurrentFont().info.note = window.textEditor.get()
    window.close()

if CurrentFont() is None:
    vanilla.dialogs.message("there is no current font, operation aborted")
else:
    window = Window((400, 400),"edit info.note", minSize=(100, 100))
    window.textEditor = TextEditor(posSize=(0, 0, 400, 300))
    noteContent = CurrentFont().info.note or ""
    window.textEditor.set(noteContent)
    window.updateNoteButton = SquareButton(posSize=(0, 350, 100, 50), title="update", callback=onSubmit)
    window.cancelButton = SquareButton(posSize=(110, 350, 100, 50), title="cancel", callback=lambda x: window.close())
    window.open()