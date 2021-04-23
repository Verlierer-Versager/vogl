import math


class point:
    def __init__(self, row: int, col: int) -> None:
        self._row = row
        self._col = col

    @property
    def row(self):
        return self._row

    @property
    def colm(self):
        return self._col


class VoglGame:
    def __init__(self, level: int) -> None:
        if 0 < level < 11:
            self._level = self.load_level(level)
            self._save = self._level.copy()
            self._current_point = None

    @staticmethod
    def load_level(level: int):
        level_data = []
        filename = "levels/level_" + str(level) + ".txt"
        with open(filename) as f:
            for line in f:
                level_data.append([int(x) for x in line.split()])
        return level_data

    @property
    def level(self):
        return self._level

    @property
    def size(self):
        return len(self._level)

    @property
    def current_point(self):
        return self._current_point

    @property
    def save(self):
        return self._save

    def restart(self):
        self._level = self._save.copy()
        self._current_point = None

    def set_current_point(self, row: int, colm: int):
        # new_point = point(row, colm)
        if self._current_point is None:
            self._current_point = point(row, colm)
            return True
        elif self._current_point.row == row and self._current_point.colm == colm:
            self._current_point = None
            return False

    @staticmethod
    def get_between(a: int, b: int):
        return (a + b) // 2

    def _is_action_correct(self, row: int, col: int) -> bool:
        return (math.fabs(self._current_point.row - row) == 2 or math.fabs(self._current_point.colm - col) == 2) and \
               self._level[self._current_point.row][self._current_point.colm] == 1 and \
               self._level[self.get_between(self._current_point.row, row)][
                   self.get_between(self._current_point.colm, col)] == 1 and self._level[row][col] == 0

    def _action_perform(self, row: int, col: int):
        self._level[self._current_point.row][self._current_point.colm] = 0
        self._level[self.get_between(self._current_point.row, row)][self.get_between(self._current_point.colm, col)] = 0
        self._level[row][col] = 1
        self._current_point = point(row, col)

    def is_level_complete(self):
        count = 0
        for i in range(len(self._level)):
            for j in range(len(self._level[i])):
                if self._level[i][j] == 1:
                    count += 1
        return count == 1

    def left_mouse_click(self, row: int, col: int) -> None:
        if self._current_point is not None and self._is_action_correct(row, col):
            self._action_perform(row, col)
        #     return True  # произошло ли действие
        # return False
