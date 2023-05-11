from PyQt5.QtGui import QColor


WindowWidth = 500
WindowHeight = 500


class Segment:
    SegmentSize = 50

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = QColor(54, 112, 160)

    def drawSegment(self, painter):
        x1, y1, x2, y2 = self.coords()

        painter.fillRect(x1 + 1, y1 + 1, Segment.SegmentSize - 2,
                         Segment.SegmentSize - 2, self.color)

        painter.setPen(self.color.lighter())
        painter.drawLine(x1, y2 - 1, x1, y1)
        painter.drawLine(x1, y1, x2 - 1, y1)

        painter.setPen(self.color.darker())
        painter.drawLine(x1 + 1, y2 - 1, x2 - 1, y2 - 1)
        painter.drawLine(x2 - 1, y2 - 1, x2 - 1, y1 + 1)

    def coords(self):
        x1 = self.x
        y1 = self.y
        x2 = self.x + Segment.SegmentSize
        y2 = self.y + Segment.SegmentSize
        return x1, y1, x2, y2


class Main_Block:
    def __init__(self, segment):
        self.segment = segment

    def collidesWithBlocks(self, blocks, direction):
        future_x = self.segment.x + Segment.SegmentSize * direction[0]
        future_y = self.segment.y + Segment.SegmentSize * direction[1]

        for block in blocks:
            if future_x != block.x or future_y != block.y:
                continue
            return True

        return False

    def move(self, direction, blocks, block_walls):
        at_boarder_window_x = bool(WindowWidth > self.segment.x + Segment.SegmentSize * direction[0] >= 0)
        at_boarder_window_y = bool(WindowHeight > self.segment.y + Segment.SegmentSize * direction[1] >= 0)


        not_colliding_wall = True

        for block_wall in block_walls:
            if not (self.segment.x + Segment.SegmentSize * direction[0] != block_wall.x or self.segment.y != block_wall.y):
                not_colliding_wall = False
                break
            elif not (self.segment.y + Segment.SegmentSize * direction[1] != block_wall.y or self.segment.x != block_wall.x):
                not_colliding_wall = False
                break

        future_x = self.segment.x + Segment.SegmentSize * direction[0]
        future_y = self.segment.y + Segment.SegmentSize * direction[1]

        flag = True
        if direction[0] != 0:
            if at_boarder_window_x and not_colliding_wall:
                for block in blocks:
                    if future_x == block.x and self.segment.y == block.y:
                        block_x = block.x
                        block.move_block(direction, block_walls, blocks)
                        if block_x == block.x:
                            flag = False
                            return
                if flag == True:
                    self.segment.x += Segment.SegmentSize*direction[0]
                    return
        elif direction[1] != 0:
            if at_boarder_window_y and not_colliding_wall:
                for block in blocks:
                    if future_y == block.y and self.segment.x == block.x:
                        block_y = block.y
                        block.move_block(direction, block_walls, blocks)
                        if block_y == block.y:
                            flag = False
                            return
                if flag ==  True:
                    self.segment.y += Segment.SegmentSize * direction[1]
                    return


class Block_Wall(Segment):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = QColor(182, 183, 187)


class Block(Segment):
    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.color_rgb = color
        self.color = self.getColor(color)

    def getColor(self, rgb):
        return QColor(rgb[0], rgb[1], rgb[2])

    def collidesWithBlocks(self, blocks, direction):
        future_x = self.x + Segment.SegmentSize * direction[0]
        future_y = self.y + Segment.SegmentSize * direction[1]

        for block in blocks:
            if future_x == block.x and future_y == block.y:
                return True

        return False

    def move_block(self, direction, block_walls, blocks):
        at_boarder_window_x = bool(WindowWidth > self.x + Segment.SegmentSize * direction[0] >= 0)
        at_boarder_window_y = bool(WindowHeight > self.y + Segment.SegmentSize * direction[1] >= 0)

        not_colliding_wall = True

        if self.collidesWithBlocks(blocks, direction):
            return

        for block_wall in block_walls:
            if not (self.x + Segment.SegmentSize * direction[0] != block_wall.x or self.y != block_wall.y):
                not_colliding_wall = False
                break
            elif not (self.y + Segment.SegmentSize * direction[1] != block_wall.y or self.x != block_wall.x):
                not_colliding_wall = False
                break

        if direction[0] != 0:
            if at_boarder_window_x and not_colliding_wall:
                self.x = self.x + Segment.SegmentSize * direction[0]
        elif direction[1] != 0 and not_colliding_wall:
            if at_boarder_window_y:
                self.y = self.y + Segment.SegmentSize * direction[1]


class Wall(Segment):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = QColor(85, 99, 99)

