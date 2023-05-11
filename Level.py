from CubiconGame import Main_Block, Segment, Block_Wall, Block


class Level:
    def __init__(self, data):
        self.main_block = Main_Block(Segment(data["main_block"][0], data["main_block"][1]))
        self.blocks = [Block(x, y, tuple(color)) for x, y, color in data["blocks"]]
        self.block_walls = [Block_Wall(x, y) for x, y in data["block_walls"]]


def process_file(filename):
    Red = (255, 0, 0)  # цвет красного блока
    Blue = (0, 0, 255)  # цвет синего блока
    Green = (0, 255, 0)

    # открываем файл и считываем его содержимое в массив
    with open(filename, "r") as f:
        lines = f.readlines()
        level_map = [list(map(int, line.split())) for line in lines]

    # проходимся по всем ячейкам массива и добавляем блоки в словарь
    blocks = []
    block_walls = []
    main_block = None
    for y, row in enumerate(level_map):
        for x, cell in enumerate(row):
            if cell == 1:
                main_block = (x * 50, y * 50)
            elif cell == 2:
                blocks.append((x * 50, y * 50, Blue))
            elif cell == 3:
                blocks.append((x * 50, y * 50, Red))
            elif cell == 4:
                blocks.append((x * 50, y * 50, Green))
            elif cell == 5:
                block_walls.append((x * 50, y * 50))

    # формируем словарь с данными
    data = {
        "main_block": main_block,
        "blocks": blocks,
        "block_walls": block_walls
    }

    return data
class Level1:
    data = process_file('level_01.txt')


class Level2:
    data = process_file('level_02.txt')


class Level3:
    data = process_file('level_03.txt')
class Level4:
    data = process_file('level_04.txt')
class Level5:
    data = process_file('level_05.txt')
