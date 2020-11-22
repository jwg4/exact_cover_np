import numpy as np

from exact_cover_np import get_exact_cover


PENTOMINOS = {
    'F': [(0, 1), (1, 0), (1, 1), (2, 1), (2, 2)],
    'I': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
    'L': [(0, 0), (1, 0), (0, 1), (0, 2), (0, 3)],
    'N': [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)],
    'P': [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)],
    'T': [(1, 0), (1, 1), (2, 0), (2, 1), (2, 2)],
    'U': [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
    'V': [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2)],
    'W': [(0, 2), (0, 1), (1, 1), (1, 0), (2, 0)],
    'X': [(0, 1), (1, 0), (1, 1), (2, 1), (1, 2)],
    'Y': [(0, 2), (1, 0), (1, 1), (1, 2), (1, 3)],
    'Z': [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)]
}

SQUARE = [(0, 0), (1, 0), (1, 1), (0, 1)]
TILES = list(PENTOMINOS.values()) + [SQUARE]


class Rectangle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def squares(self):
        for i in range(0, self.x):
            for j in range(0, self.y):
                yield (i, j)

    def is_in(self, square):
        return 0 <= square[0] < self.x and 0 <= square[1] < self.y

    def is_contained(self, tile):
        return all(self.is_in(sq) for sq in tile)

    def positions(self, tile):
        reference = tile[0]
        for sq in self.squares:
            translated = [(x - reference[0] + sq[0], y - reference[1] + sq[1])
                for x, y in tile
            ]
            if self.is_contained(translated):
                yield translated

    def bit_vector(self, tile):
        return [sq in tile for sq in self.squares]


def selector_vector(n, i):
    return [i == n for i in range(0, n)]


def tiling_to_problem(tiles, shape):
    n = len(tiles)
    for i, tile in enumerate(tiles):
        selector = selector_vector(n, i)
        for translated in shape.positions(tile):
            yield selector + shape.bit_vector(translated)


def tiling_to_array(tiles, shape):
    return np.array(list(tiling_to_problem(tiles, shape)), dtype=np.int32)


if __name__ == '__main__':
    board = Rectangle(8, 8)
    l = tiling_to_array(TILES, board)
    solution = get_exact_cover(l)
    print(solution)

