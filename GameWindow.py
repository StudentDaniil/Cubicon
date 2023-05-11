from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QPushButton

from Level import *
from MainWindowUI4 import Ui_MainWindow as MainWindowUI

from Board import Board


class GameWindow(QtWidgets.QMainWindow, MainWindowUI):
    Width = 500
    Height = 525

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.level_list = ['Level1', 'Level2', 'Level3']  # список уровней

    def start_level(self, level_name):
        level_data = None
        if level_name == 'Level1':
            level_data = Level1.data
        elif level_name == 'Level2':
            level_data = Level2.data
        elif level_name == 'Level3':
            level_data = Level3.data
        elif level_name == 'Level4':
            level_data = Level4.data
        elif level_name == 'Level5':
            level_data = Level5.data

        if level_data:
            self.board = Board(self)  # создание экземпляра класса Board  # инициализация экземпляра класса Board
            self.setCentralWidget(self.board)
            self.board.start_level(level_data)

    def initUI(self):
        self.board = Board(self)

        self.setCentralWidget(self.board)

        self.resize(GameWindow.Width, GameWindow.Height)
        self.center()
        self.setWindowTitle('Cubicon')

        self.show()

    def update_view(self):
        self.gameFieldTableView.viewport().update()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                  (screen.height() - size.height()) // 2)

