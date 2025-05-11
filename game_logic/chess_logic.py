from copy import deepcopy


class Chess:
    def __init__(
        self, fen_str="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    ):
        self.field = [
            [None for _ in range(8)] for _ in range(8)
        ]  # Создаём пустую доску
        # Словарь для преобразования символов FEN в классы фигур
        piece_map = {
            "r": Rook,
            "n": Knight,
            "b": Bishop,
            "q": Queen,
            "k": King,
            "p": Pawn,
        }

        # Разбиваем FEN на компоненты
        fen_parts = fen_str.split()
        rows = fen_parts[0].split("/")

        # Заполняем поле
        for y, row in enumerate(rows):
            y_converted = 7 - y  # FEN начинается с 8-го ряда (y=7 в нашей системе)
            x = 0
            for char in row:
                if char.isdigit():
                    x += int(char)  # Пропускаем пустые клетки
                else:
                    color = "white" if char.isupper() else "black"
                    piece_class = piece_map[char.lower()]
                    self.field[y_converted][x] = piece_class(x, y_converted, color)
                    x += 1

        # Устанавливаем очередь хода
        self.who_walking = "white" if fen_parts[1] == "w" else "black"

        self.castling_rights = {
            "K": "K" in fen_parts[2],
            "Q": "Q" in fen_parts[2],
            "k": "k" in fen_parts[2],
            "q": "q" in fen_parts[2],
        }
        if fen_parts[3] == "-":
            self.en_passant = None
        else:
            self.en_passant = ord(fen_parts[3][0]) - 97, 8 - int(fen_parts[3][1])
        self.halfmove_clock = int(fen_parts[4])
        self.fullmove_number = int(fen_parts[5])

        self.to_who = None
        self.shah = self.is_shah("white") or self.is_shah("black")
        if self.shah:
            self.mate = self.is_mate(self.to_who)
            self.stalemate = False
            self.draw = False
        else:
            self.mate = False
            self.stalemate = self.is_stalemate()
            self.draw = self.is_draw()

    def get_fen(self):
        """Конвертирует текущую позицию в FEN-строку."""
        piece_map = {
            Pawn: "p",
            Rook: "r",
            Knight: "n",
            Bishop: "b",
            Queen: "q",
            King: "k",
        }
        fen_rows = []
        for row in reversed(self.field):
            fen_row = []
            empty = 0

            for cell in row:
                if cell is None:
                    empty += 1
                else:
                    if empty > 0:
                        fen_row.append(str(empty))
                        empty = 0
                    symbol = piece_map[type(cell)]
                    fen_row.append(symbol.upper() if cell.color == "white" else symbol)

            if empty > 0:
                fen_row.append(str(empty))
            fen_rows.append("".join(fen_row))

        turn = "w" if self.who_walking == "white" else "b"

        castling = []
        if self.castling_rights["K"]:
            castling.append("K")
        if self.castling_rights["Q"]:
            castling.append("Q")
        if self.castling_rights["k"]:
            castling.append("k")
        if self.castling_rights["q"]:
            castling.append("q")
        castling_str = "".join(castling) if castling else "-"

        en_passant = (
            chr(97 + self.en_passant[0]) + str(8 - self.en_passant[1])
            if self.en_passant
            else "-"
        )

        halfmove_clock = str(self.halfmove_clock)
        fullmove_number = str(self.fullmove_number)

        return " ".join(
            [
                "/".join(fen_rows),
                turn,
                castling_str,
                en_passant,
                halfmove_clock,
                fullmove_number,
            ]
        )

    def find_king_position(self, color):
        for y in range(8):
            for x in range(8):
                if (
                    isinstance(self.field[y][x], King)
                    and self.field[y][x].color == color
                ):
                    return self.field[y][x].x, self.field[y][x].y

    def is_current_player_figure(self, x, y):
        """Проверка есть фигура в клетке и принадлежит ли она цвету, который сейчас ходит"""
        if self.field[y][x] is None:
            return False
        if self.who_walking != self.field[y][x].color:
            return False
        return True

    def can_move(self, x, y, new_x, new_y):
        """Проверка может ли фигура сходить"""
        if not self.is_current_player_figure(x, y):
            return False
        if not self.field[y][x].can_move(new_x, new_y, self.field) or (
            self.en_passant
            and isinstance(self.field[y][x], Pawn)
            and not self.field[y][x].can_move(new_x, new_y, self.field, self.en_passant)
            or (
                isinstance(self.field[y][x], King)
                and not self.can_castle(x, y, new_x, new_y)
            )
        ):
            # Может ли фигура переместиться в данную клетку
            return False
        # Может ли сходить фигура так, чтобы короля не срубили в следующем ходу

        # Сохраняем состояние
        figure = self.field[y][x]
        original_block = self.field[new_y][new_x]

        # Делаем временный ход
        self.field[y][x] = None
        self.field[new_y][new_x] = figure
        figure.x, figure.y = new_y, new_y

        is_shah = self.is_shah(self.who_walking)

        # Восстанавливаем состояние
        self.field[y][x] = figure
        self.field[new_y][new_x] = original_block
        figure.x, figure.y = x, y

        if is_shah:
            return False

        return True

    def can_castle(self, x, y, new_x, new_y):
        if not (y - new_y == 0 and abs(x - new_x) == 2):
            return False
        king = self.field[y][x]
        if king.moved:
            return False

        direction = new_x - x
        rook_x = 7 if direction > 0 else 0
        rook = self.field[y][rook_x]

        if not isinstance(rook, Rook) or rook.moved:
            return False

        step = 1 if direction > 0 else -1
        for dx in range(1, abs(direction)):
            if self.field[y][x + dx * step] is not None:
                return False

        if self.is_shah(king.color):
            return False

        temp_chess = deepcopy(self)
        temp_king = temp_chess.field[y][x]
        temp_chess.field[y][x] = None
        temp_chess.field[y][x + step] = temp_king
        temp_king.x += step
        if temp_chess.is_shah(king.color):
            return False

        temp_chess.field[y][x + step] = None
        temp_chess.field[y][new_x] = temp_king
        temp_king.x = new_x
        return not temp_chess.is_shah(king.color)

    def move(self, x, y, new_x, new_y):
        """Перемещение фигуры"""
        if not self.can_move(x, y, new_x, new_y):
            return False

        if isinstance(self.field[y][x], King):
            self.castling_rights["K" if self.field[y][x].color == "white" else "k"] = (
                False
            )
            self.castling_rights["Q" if self.field[y][x].color == "white" else "q"] = (
                False
            )
            self.field[y][x].moved = True
        if isinstance(self.field[y][x], Rook):
            if x == 0:
                self.castling_rights[
                    "Q" if self.field[y][x].color == "white" else "q"
                ] = False
            else:
                self.castling_rights[
                    "K" if self.field[y][x].color == "white" else "k"
                ] = False
            self.field[y][x].moved = True
        if self.field[new_y][new_x] or isinstance(self.field[y][x], Pawn):
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        if self.who_walking == "black":
            self.fullmove_number += 1

        self.field[y][x], self.field[new_y][new_x] = None, self.field[y][x]
        self.field[new_y][new_x].x, self.field[new_y][new_x].y = new_x, new_y

        if isinstance(self.field[new_y][new_x], King) and abs(new_x - x) == 2:
            direction = new_x - x
            rook_x = 7 if direction > 0 else 0
            rook_new_x = new_x - 1 if direction > 0 else new_x + 1
            rook = self.field[y][rook_x]
            self.field[y][rook_x] = None
            self.field[y][rook_new_x] = rook
            rook.x = rook_new_x
            rook.moved = True
            self.castling_rights["K" if rook.color == "white" else "k"] = False
            self.castling_rights["Q" if rook.color == "white" else "q"] = False

        if (
            isinstance(self.field[new_y][new_x], Pawn)
            and (new_x, new_y) == self.en_passant
        ):
            if self.field[new_y][new_x].color == "white":
                captured_y = new_y + 1
            else:
                captured_y = new_y - 1
            self.field[captured_y][new_x] = None

        if isinstance(self.field[new_y][new_x], Pawn) and abs(y - new_y) == 2:
            self.en_passant = x, (y + new_y) // 2
        else:
            self.en_passant = None

        if isinstance(self.field[new_y][new_x], Pawn):
            if (self.field[new_y][new_x].color == "white" and new_y == 0) or (
                self.field[new_y][new_x].color == "black" and new_y == 7
            ):
                # Заменяем пешку на ферзя
                self.field[new_y][new_x] = Queen(
                    new_x, new_y, self.field[new_y][new_x].color
                )
        self.who_walking = "black" if self.who_walking == "white" else "white"
        return True

    def is_shah(self, color):
        """Обьявлен ли королю шах"""
        king_x, king_y = self.find_king_position(color)
        for y in range(8):
            for x in range(8):
                if self.field[y][x] and self.field[y][x].color != color:
                    if self.field[y][x].can_move(king_x, king_y, self.field):
                        self.to_who = color
                        return True
        return False

    def is_mate(self, color):
        """Проверка, находится ли игрок под матом."""
        if not self.is_shah(color):
            return False

        for y in range(8):
            for x in range(8):
                if not self.is_current_player_figure(x, y):
                    continue
                for new_y in range(8):
                    for new_x in range(8):
                        if self.can_move(x, y, new_x, new_y):
                            temp_chess = deepcopy(self)
                            original_color = temp_chess.who_walking
                            success = temp_chess.move(x, y, new_x, new_y)
                            if success and not temp_chess.is_shah(original_color):
                                return False
        return True

    def is_stalemate(self):
        """Проверяет, находится ли игрок в патовой ситуации."""

        # Проверяем, есть ли хотя бы один допустимый ход у игрока
        for y in range(8):
            for x in range(8):
                if not self.is_current_player_figure(x, y):
                    continue
                # Проверяем все возможные клетки для хода
                for new_y in range(8):
                    for new_x in range(8):
                        if self.can_move(x, y, new_x, new_y):
                            return False  # Найден допустимый ход -> пат отсутствует
        return True  # Нет допустимых ходов -> пат

    def is_draw(self):
        if self.halfmove_clock >= 100:
            return True

        pieces = []
        for row in self.field:
            for piece in row:
                if piece:
                    pieces.append(piece)

        # Только короли
        if len(pieces) == 2:
            return True

        # Король + 1 легкая фигура
        if len(pieces) == 3:
            for p in pieces:
                if isinstance(p, (Knight, Bishop)):
                    return True
        return False


class Figure:
    def __init__(self, x: int, y: int, color: str):
        self.x, self.y, self.color = x, y, color


class Pawn(Figure):  # Пешка
    def can_move(
        self, new_x: int, new_y: int, field: list[list], en_passant: tuple = None
    ):
        if self.color == "white":
            # Обычный ход или взятие
            if new_x == self.x:
                if not (self.y - new_y == 1 or (self.y - new_y == 2 and self.y == 6)):
                    return False
                # Проверка на препятствия
                for i in range(new_y, self.y):
                    if field[i][new_x] is not None:
                        return False
            elif abs(new_x - self.x) == 1:
                # Обычное взятие или взятие на проходе
                if self.y - new_y != 1:
                    return False
                # Проверка на фигуру противника или en_passant
                target_cell = field[new_y][new_x]
                if target_cell is None:
                    # Проверка на en_passant
                    if en_passant == (new_x, new_y):
                        # Пешка противника должна быть на (new_x, new_y + 1)
                        adjacent_pawn = field[new_y + 1][new_x]
                        return (
                            isinstance(adjacent_pawn, Pawn)
                            and adjacent_pawn.color != self.color
                        )
                    return False
                else:
                    return target_cell.color != self.color
            else:
                return False
        elif self.color == "black":
            if new_x == self.x:
                if not (new_y - self.y == 1 or (new_y - self.y == 2 and self.y == 1)):
                    return False
                for i in range(self.y + 1, new_y + 1):
                    if field[i][new_x] is not None:
                        return False
            elif abs(new_x - self.x) == 1:
                if new_y - self.y != 1:
                    return False
                target_cell = field[new_y][new_x]
                if target_cell is None:
                    # Проверка на en_passant
                    if en_passant == (new_x, new_y):
                        adjacent_pawn = field[new_y - 1][new_x]
                        return (
                            isinstance(adjacent_pawn, Pawn)
                            and adjacent_pawn.color != self.color
                        )
                    return False
                else:
                    return target_cell.color != self.color
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
    def __init__(self, x: int, y: int, color: str):
        super().__init__(x, y, color)
        self.moved = False

    def can_move(self, new_x: int, new_y: int, field: list[list]):
        if not (abs(self.x - new_x) <= 1 and abs(self.y - new_y) <= 1):
            # Проверка может ли физически переместиться в данную клетку
            return False
        if field[new_y][new_x] is not None and field[new_y][new_x].color == self.color:
            # Проверка не пытается ли съесть своих
            return False
        return True


class Rook(Figure):  # Ладья
    def __init__(self, x: int, y: int, color: str):
        super().__init__(x, y, color)
        self.moved = False

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


class Bishop(Figure):  # Офицер
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
