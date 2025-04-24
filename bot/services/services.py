from lexicon.lexicon import LEXICON


class Chess:
    def __init__(self):
        self.who_walking = "white"
        self.field = [
            [
                Rook(0, 0, color="black"),
                Knight(1, 0, color="black"),
                Officer(2, 0, color="black"),
                Queen(3, 0, color="black"),
                King(4, 0, color="black"),
                Officer(5, 0, color="black"),
                Knight(6, 0, color="black"),
                Rook(7, 0, color="black"),
            ],
            [Pawn(i, 1, color="black") for i in range(8)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn(i, 6, color="white") for i in range(8)],
            [
                Rook(0, 7, color="white"),
                Knight(1, 7, color="white"),
                Officer(2, 7, color="white"),
                Queen(3, 7, color="white"),
                King(4, 7, color="white"),
                Officer(5, 7, color="white"),
                Knight(6, 7, color="white"),
                Rook(7, 7, color="white"),
            ],
        ]

    def can_move(self, x, y):
        if self.field[y][x] is None:
            return False
        if self.who_walking != self.field[y][x].color:
            return False
        return True

    def move(self, x, y, new_x, new_y):
        if self.field[y][x] is None:
            return False
        if self.who_walking != self.field[y][x].color:
            return False
        if not self.field[y][x].can_move(new_x, new_y, self.field):
            return False

        self.field[y][x], self.field[new_y][new_x] = None, self.field[y][x]
        self.field[new_y][new_x].x, self.field[new_y][new_x].y = new_x, new_y

        shah_figure = self.is_shah(self.who_walking)
        if shah_figure is not None:
            self.field[y][x], self.field[new_y][new_x] = self.field[new_y][new_x], None
            self.field[y][x].x, self.field[y][x].y = x, y
            return False

        self.who_walking = "black" if self.who_walking == "white" else "white"
        return True

    def is_shah(self, color):
        flag_search = False
        for i in self.field:
            for j in i:
                if not flag_search and isinstance(j, King) and j.color == color:
                    x, y = j.x, j.y
                    flag_search = True
                    break
            if flag_search:
                break

        for i in range(8):
            for j in range(8):
                if (
                    y == i
                    or x == j
                    or abs(y - i) == abs(x - j)
                    or (abs(y - i) == 2 and abs(x - j) == 1)
                    or (abs(y - i) == 1 and abs(x - j) == 2)
                ):
                    if (
                        self.field[i][j] is not None
                        and self.field[i][j].color != self.field[y][x].color
                        and self.field[i][j].can_move(x, y, self.field)
                    ):
                        return self.field[i][j]

    def is_mate(self, figure):
        1


class Figure:
    def __init__(self, x: int, y: int, color: str):
        self.x, self.y, self.color = x, y, color

    def __str__(self):
        return LEXICON[self.color][self.__class__.__name__]


class Pawn(Figure):  # Пешка
    def can_move(self, new_x: int, new_y: int, field: list[list]):
        if self.color == "white":
            if new_x == self.x:
                if not (self.y - new_y == 1 or (self.y - new_y == 2 and self.y == 6)):
                    return False
                for i in range(new_y, self.y):
                    if field[i][new_x] is not None:
                        return False
            elif abs(new_x - self.x) == 1:
                if not self.y - new_y == 1:
                    return False
                if (
                    field[new_y][new_x] is None
                    or field[new_y][new_x].color == self.color
                ):
                    return False
            else:
                return False
        elif self.color == "black":
            if new_x == self.x:
                if not (self.y - new_y == -1 or (self.y - new_y == -2 and self.y == 1)):
                    return False
                for i in range(new_y, self.y, -1):
                    if field[i][new_x] is not None:
                        return False
            elif abs(new_x - self.x) == 1:
                if not self.y - new_y == -1:
                    return False
                if (
                    field[new_y][new_x] is None
                    or field[new_y][new_x].color == self.color
                ):
                    return False
            else:
                return False
        return True


class Queen(Figure):  # Ферзь
    def can_move(self, new_x: int, new_y: int, field: list[list]):
        if not (
            abs(self.x - new_x) == abs(self.y - new_y)
            or self.x == new_x
            or self.y == new_y
        ):
            # Проверка может ли физически переместиться в данную клетку
            return False
        if field[new_y][new_x] is not None and field[new_y][new_x].color == self.color:
            # Проверка не пытается ли съесть своих
            return False
        if abs(self.x - new_x) == abs(self.y - new_y):
            # Проверка есть ли фигуры на пути к точке
            step_x, step_y = abs(new_x - self.x) // (new_x - self.x), abs(
                new_y - self.y
            ) // (new_y - self.y)
            old_x, old_y = self.x, self.y
            while abs(old_x - new_x) != 1:
                old_x += step_x
                old_y += step_y
                if field[old_y][old_x] is not None:
                    return False
        if self.x == new_x or self.y == new_y:
            # Проверка есть ли фигуры на пути к точке
            if abs(self.x - new_x) > 1:
                for j in range(min(self.x, new_x) + 1, max(self.x, new_x)):
                    if field[self.y][j] is not None:
                        return False
            if abs(self.y - new_y) > 1:
                for i in range(min(self.y, new_y) + 1, max(self.y, new_y)):
                    if field[i][self.x] is not None:
                        return False
        return True


class King(Figure):  # Король
    def can_move(self, new_x: int, new_y: int, field: list[list]):
        if not (abs(self.x - new_x) <= 1 and abs(self.y - new_y) <= 1):
            # Проверка может ли физически переместиться в данную клетку
            return False
        if field[new_y][new_x] is not None and field[new_y][new_x].color == self.color:
            # Проверка не пытается ли съесть своих
            return False
        return True


class Officer(Figure):  # Офицер
    def can_move(self, new_x: int, new_y: int, field: list[list]):
        if not (abs(self.x - new_x) == abs(self.y - new_y)):
            # Проверка может ли физически переместиться в данную клетку
            return False
        if field[new_y][new_x] is not None and field[new_y][new_x].color == self.color:
            # Проверка не пытается ли съесть своих
            return False
        # Проверка есть ли фигуры на пути к точке
        step_x, step_y = abs(new_x - self.x) // (new_x - self.x), abs(
            new_y - self.y
        ) // (new_y - self.y)
        old_x, old_y = self.x, self.y
        while abs(old_x - new_x) != 1:
            old_x += step_x
            old_y += step_y
            if field[old_y][old_x] is not None:
                return False
        return True


class Rook(Figure):  # Ладья
    def can_move(self, new_x: int, new_y: int, field: list[list]):
        if not (self.x == new_x or self.y == new_y):
            # Проверка может ли физически переместиться в данную клетку
            return False
        if field[new_y][new_x] is not None and field[new_y][new_x].color == self.color:
            # Проверка не пытается ли съесть своих
            return False
        # Проверка есть ли фигуры на пути к точке
        if abs(self.x - new_x) > 1:
            for j in range(min(self.x, new_x) + 1, max(self.x, new_x)):
                if field[self.y][j] is not None:
                    return False
        if abs(self.y - new_y) > 1:
            for i in range(min(self.y, new_y) + 1, max(self.y, new_y)):
                if field[i][self.x] is not None:
                    return False
        return True


class Knight(Figure):  # Конь
    def can_move(self, new_x: int, new_y: int, field: list[list]):
        if not (
            (abs(self.x - new_x) == 1 and abs(self.y - new_y) == 2)
            or (abs(self.x - new_x) == 2 and abs(self.y - new_y) == 1)
        ):
            # Проверка может ли физически переместиться в данную клетку
            return False
        if field[new_y][new_x] is not None and field[new_y][new_x].color == self.color:
            # Проверка не пытается ли съесть своих
            return False
        return True


session_dict = {}
