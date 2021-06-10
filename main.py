import qdarkstyle
from PyQt5 import QtWidgets

import sys
from image_convert_gui import MyWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QtWidgets.QApplication([])
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)
    win = MyWindow()
    win.show()
    app.exec_()
