from typing import List, Union, Tuple
from random import seed, randint


class TagModel:

    __slots__ = ['_width', '_height', '_movable_chips', '_free_space', '_chip_pos', '_map']

    _width: int
    _height: int
    _movable_chips: List[int]
    _free_space: int
    _chip_pos: List[int]
    _map: List[Union[None, int]]

    def __init__(self, width: int, height: int):
        assert width > 1 and height > 1
        self._width = width
        self._height = height

        self._map = [*range(width * height)]
        self._map[-1] = None
        self._chip_pos = [*range(width * height - 1)]

        self._free_space = width * height - 1
        self._movable_chips = [
            self._map[self._free_space - 1],
            self._map[width * (height-1) - 1]
        ]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def free_space_coords(self) -> Tuple[int, int]:
        return self._free_space % self._width, self._free_space // self._width

    def get_chip_coords(self, chip_idx: int) -> Tuple[int, int]:
        assert 0 <= chip_idx < len(self._chip_pos)
        pos = self._chip_pos[chip_idx]
        return pos % self._width, pos // self._width

    def get_chip_idx_at(self, x: int, y: int) -> Union[None, int]:
        assert 0 <= x < self._width and 0 <= y < self._height
        return self._map[x + y * self._width]

    def get_movable_chips_coods(self) -> List[Tuple[int, int]]:
        return [(idx % self._width, idx // self._width) for idx in self._movable_chips]

    def is_chip_movable(self, idx: int) -> bool:
        return idx in self._movable_chips

    def __update_movable_chips(self):
        self._movable_chips.clear()
        idx = self._free_space
        x, y = idx % self._width, idx // self._width

        if x > 0:
            self._movable_chips.append(self._map[x-1 + y*self._width])
        if x < self._width - 1:
            self._movable_chips.append(self._map[x+1 + y * self._width])
        if y > 0:
            self._movable_chips.append(self._map[x + (y-1) * self._width])
        if y < self._height - 1:
            self._movable_chips.append(self._map[x + (y+1) * self._width])

    def move_chip(self, chip_idx: int):
        assert self.is_chip_movable(chip_idx)
        chip_pos = self._chip_pos[chip_idx]
        self._chip_pos[chip_idx] = self._free_space
        self._map[self._free_space] = chip_idx
        self._map[chip_pos] = None
        self._free_space = chip_pos
        self.__update_movable_chips()

    def check_win(self) -> bool:
        return all(j == idx for j, idx in enumerate(self._chip_pos))

    def shuffle(self):
        seed(None)
        prev_idx = None
        counter = 0
        while counter < 100:
            move_idx = self._movable_chips[randint(0, len(self._movable_chips)-1)]
            if move_idx == prev_idx:
                continue
            self.move_chip(move_idx)
            prev_idx = move_idx
            counter += 1
