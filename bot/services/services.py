from lexicon.lexicon import LEXICON


# Написать рокировку, взятие на проходе, перевоплощение пешки на конце доски
class Chess:
    def __init__(self):
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
        self.white_king = self.field[7][4]  # Переменная белого короля
        self.black_king = self.field[0][4]  # Переменная чёрного короля
        self.who_walking = "white"  # Переменная для отслеживания какой цвет ходит
        self.is_finished = None  # Переменная для отслеживания окончена ли игра

    def is_figure(self, x, y):
        """Проверка есть фигура в клетке и принадлежит ли она цвету, который сейчас ходит"""
        if self.field[y][x] is None:
            return False
        if self.who_walking != self.field[y][x].color:
            return False
        return True

    def can_move(self, x, y, new_x, new_y):
        """Проверка может ли фигура сходить"""
        if not self.is_figure(x, y):
            return False
        if not self.field[y][x].can_move(new_x, new_y, self.field):
            # Может ли фигура переместиться в данную клетку
            return False

        # Может ли сходить фигура так, чтобы короля не срубили в следующем ходу
        self.field[y][x].x, self.field[y][x].y = new_x, new_y
        old = self.field[new_y][new_x]
        self.field[y][x], self.field[new_y][new_x] = None, self.field[y][x]
        shah_figure = self.is_shah(self.who_walking)
        self.field[y][x], self.field[new_y][new_x] = self.field[new_y][new_x], old
        self.field[y][x].x, self.field[y][x].y = x, y

        if shah_figure is not None:
            return "shah"

        return True

    def move(self, x, y, new_x, new_y):
        """Перемещение фигуры"""
        can_move = self.can_move(x, y, new_x, new_y)
        if can_move != True:
            return self.can_move(x, y, new_x, new_y)

        self.field[y][x], self.field[new_y][new_x] = None, self.field[y][x]
        self.field[new_y][new_x].x, self.field[new_y][new_x].y = new_x, new_y

        self.who_walking = "black" if self.who_walking == "white" else "white"
        self.is_mate()

    def is_shah(self, color):
        """Обьявлен ли королю шах"""
        if color == "white":
            x, y = self.white_king.x, self.white_king.y
        else:
            x, y = self.black_king.x, self.black_king.y

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

    def is_mate(
        self,
    ):
        """Обьявлен ли королю шах и мат"""
        shah_figure = self.is_shah(self.who_walking)
        if shah_figure is None:
            return
        if self.who_walking == "white":
            x, y = self.white_king.x, self.white_king.y
        else:
            x, y = self.black_king.x, self.black_king.y

        for i in range(max(y - 1, 0), min(y + 1, 7) + 1):
            for j in range(max(x - 1, 0), min(x + 1, 7) + 1):
                if self.can_move(x, y, j, i):
                    return

        if isinstance(shah_figure, Knight):
            for i in range(8):
                for j in range(8):
                    if (
                        self.field[i][j] is not None
                        and self.field[i][j].color == self.who_walking
                        and not isinstance(self.field[i][j], King)
                        and self.field[i][j].can_move(x, y, self.field)
                    ):
                        return
        else:
            x1, y1 = shah_figure.x, shah_figure.y
            x2, y2 = x, y
            step_x, step_y = abs(x2 - x1) // (x2 - x1), abs(y2 - y1) // (y2 - y1)
            for i in range(8):
                for j in range(8):
                    if (
                        self.field[i][j] is not None
                        and self.field[i][j].color == self.who_walking
                        and not isinstance(self.field[i][j], King)
                    ):
                        x1, y1 = shah_figure.x, shah_figure.y
                        while x1 != x2 or y1 != y2:
                            if self.field[i][j].can_move(x1, y1, self.field):
                                return
                            if x1 != x2:
                                x1 += step_x
                            if y1 != y2:
                                y1 += step_y
        self.is_finished = "black" if self.who_walking == "white" else "white"


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
