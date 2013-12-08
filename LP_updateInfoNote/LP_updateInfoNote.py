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