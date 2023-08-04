import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from src.controllers.controladores import MainController, NewRecipeController, AddIngredientsController


class Application:
    def __init__(self):
        useGUI = not '-no-gui' in sys.argv
        self.__qapplication = QApplication(sys.argv) if useGUI else QCoreApplication(sys.argv)
        self.__qwidget = None
        self.__ui = list()

    def begin(self):
        self.ui_config("main")
        return self.__qapplication.exec_()

    def ui_config(self, ui=None, parent=None, remove=None, data=None):
        trash = None
        if remove:
            trash = self.__ui.pop()

        if ui == "main":
            self.__ui.append(MainController(self))
        elif ui == "nueva receta":
            self.__ui.append(NewRecipeController(self, owner=parent, receta=data))
        elif ui == "ingredientes":
            self.__ui.append(AddIngredientsController(self, owner=parent))
        elif ui == "ver receta":
            #self.__ui.append(MainController(self, owner=parent, recipe=data))
            pass

        if trash:
            trash.hide()
            trash.close()
            del trash

        try:
            self.__ui[-1].show()
        except:
            pass


if __name__ == '__main__':
    application = Application()
    application.begin()
