import mojo
from vanilla import *
from vanilla.dialogs import getFolder

class FolderPicker(object):

    #------------
    # attributes
    #------------

    _title = 'add images to currentFont'
    _row_height = 20
    _button_height = 30
    _padding = 10
    _width = 180
    _height = (_row_height * 1) + (_button_height * 2) + (_padding * 5) + 2

    _folder_path = None

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # ufos folder
        x = self._padding
        y = self._padding
        self.w.ufos_get_folder_button = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "select bitmap folder",
                    sizeStyle="small",
                    callback=self.ufos_get_folder_callback)
        
        # open window
        self.w.open()


    # callbacks

    def ufos_get_folder_callback(self, sender):
        maybe_folder_path = getFolder()
        if maybe_folder_path:
            self._folder_path = maybe_folder_path[0]

        print maybe_folder_path



# test

folderPicker = FolderPicker()