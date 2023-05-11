from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QColor, QPainter, QFont
from PyQt5.QtWidgets import QFrame

from CubiconGame import Segment
from Level import Level1, Level
from utils import count


class Board(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.speed = 200
        self.timer = QBasicTimer()

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.isWin = False
        self.level = None  # объект класса Level
        self.blocks = []  # список объектов Block
        self.block_walls = []
        self.start_level(Level1.data)

    def start_level(self, level_data):
        self.level = Level(level_data)  # инициализация уровня данными
        self.blocks = []  # очистка списка объектов Block
        self.block_walls = []  # очистка списка объектов BlockWall

        self.main_block = self.level.main_block  # получение объекта main_block из уровня
        self.blocks += self.level.blocks  # добавление объектов block из уровня в список
        self.block_walls = self.level.block_walls  # получение списка объектов block_wall из уровня

        self.isPaused = False
        self.isStarted = True
        self.timer.start(self.speed, self)
        self.update()

    def pause(self):
        if not self.isStarted:
            return
        self.isPaused = not self.isPaused
        if self.isPaused:
            self.timer.stop()
        else:
            self.timer.start(self.speed, self)
        self.update()

    def chek_win(self, blocks):
        item_color = None
        direction_left = (-1, 0)
        direction_right = (1, 0)
        direction_up = (0, -1)
        direction_down = (0, 1)

        mass_color = count(blocks)

        flag_color = 0

        for i, block1 in enumerate(blocks):
            k_color1 = 1
            for j, block2 in enumerate(blocks[i + 1:], i + 1):
                if block1 != block2:
                    future_x_left = block1.x + Segment.SegmentSize * direction_left[0]
                    future_x_right = block1.x + Segment.SegmentSize * direction_right[0]
                    future_y_up = block1.y + Segment.SegmentSize * direction_up[1]
                    future_y_down = block1.y + Segment.SegmentSize * direction_down[1]

                    color_block1 = block1.color_rgb
                    color_block2 = block2.color_rgb

                    flag = ((future_x_left == block2.x and block1.y == block2.y) or (
                            future_x_right == block2.x and block1.y == block2.y) or (
                                    future_y_down == block2.y and block1.x == block2.x) or (
                                    future_y_up == block2.y and block1.x == block2.x))
                    if color_block1 == color_block2:
                        k_color1 += 1
                        for item in mass_color.items():
                            if color_block1 == item[0]:
                                item_color = item[1]
                                if k_color1 == item_color and flag:
                                    flag_color += 1
                                    break
        if flag_color == len(mass_color):
            self.isWin = True
            return

        self.isWin = False

    def stop(self):
        self.isStarted = False
        self.timer.stop()
        self.update()

    def paintEvent(self, event):
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color:" + QColor(255, 231, 109).name())
        painter = QPainter(self)

        for block in self.blocks:
            block.drawSegment(painter)

        self.main_block.segment.drawSegment(painter)

        for block_wall in self.block_walls:
            block_wall.drawSegment(painter)

        if self.isWin:
            painter.setPen(QColor(0, 0, 0))
            painter.setFont(QFont('Arial Rounded MT Bold', 15))
            painter.drawText(event.rect(), Qt.AlignCenter, "YOU WIN")
            self.stop()
        elif self.isPaused:
            painter.setPen(QColor(0, 0, 0))
            painter.setFont(QFont('Arial Rounded MT Bold', 30))
            painter.drawText(event.rect(), Qt.AlignCenter, "PAUSE")
        elif not self.isStarted:
            painter.setPen(QColor(0, 0, 0))
            painter.setFont(QFont('Arial Rounded MT Bold', 30))
            painter.drawText(event.rect(), Qt.AlignCenter, "GAME OVER")

        painter.end()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            pass
            self.chek_win(self.blocks)
            # движение main_block и взаимодействие со всеми блоками и стенами
        else:
            super(Board, self).timerEvent(event)
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Down or key == Qt.Key_S:
            self.main_block.move((0, 1), self.blocks, self.block_walls)
        elif key == Qt.Key_Up or key == Qt.Key_W:
            self.main_block.move((0, -1), self.blocks, self.block_walls)
        elif key == Qt.Key_Left or key == Qt.Key_A:
            self.main_block.move((-1, 0), self.blocks, self.block_walls)
        elif key == Qt.Key_Right or key == Qt.Key_D:
            self.main_block.move((1, 0), self.blocks, self.block_walls)
        elif key == Qt.Key_N:
            self.start()
        elif key == Qt.Key_P:
            self.pause()
        else:
            super(Board, self).keyPressEvent(event)
        self.update()
