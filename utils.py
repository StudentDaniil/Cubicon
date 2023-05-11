from collections import Counter


def count(blocks):
    temp_mass = []
    for block in blocks:
        temp_mass.append(block.color_rgb)
    count_color = Counter(temp_mass)
    return count_color