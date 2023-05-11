import sys
import traceback

from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QMessageBox

from GameWindow import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()


    def exception_hook(type_, value, tb):
        msg = '\n'.join(traceback.format_exception(type_, value, tb))
        # print(msg)
        QMessageBox.critical(window, 'Unhandled top level exception', msg)


    sys.excepthook = exception_hook

    window.show()
    sys.exit(app.exec_())
