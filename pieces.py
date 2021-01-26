import copy

class Piece:
    def __init__(self, color, row, col, number):
        self.color = color
        self.active = False
        self.row = row
        self.col = col
        self.number = number
        self.blocked = False
        self.captured_num = 0
        self.moves_pos = []
        self.captured_pieces = []

    def move(self, row, col):
        self.row = row
        self.col = col

    def first_move(self, board):
        pass

    def next_moves(self, board, row, col, possible_moves,
                   captured_pos, previous_pos, captures_num):
        pass


class Man(Piece):
    dark = ((1, -1), (1, 1))
    light = ((-1, -1), (-1, 1))

    def __init__(self, color, row, col, number):
        super().__init__(color, row, col, number)

    def first_move(self, board):
        self.captured_num = 0
        self.moves_pos = []
        self.captured_pieces = []
        possible_moves = []
        next_move = False

        if self.color == "light":
            moves = self.light
            capture_moves = self.dark
        else:
            moves = self.dark
            capture_moves = self.light

        for move in moves:
            x, y = move

            if self.row+x < 0 or self.row+x >= 8 \
                    or self.col+y < 0 or self.col+y >= 8:
                continue

            if board[self.row+x, self.col+y] is None:
                if not next_move:
                    possible_moves.append((self.row+x, self.col+y))
            else:
                if board[self.row+x, self.col+y].color == self.color:
                    continue

                if self.row+x+x < 0 or self.row+x+x >= 8 \
                        or self.col+y+y < 0 or self.col+y+y >= 8:
                    continue

                if board[self.row+x+x, self.col+y+y] is None:
                    next_move = True
                    self.next_moves(
                        board, self.row + x + x, self.col + y + y,
                        [(self.row + x + x, self.col + y + y)],
                        [(self.row + x, self.col + y)], move, 1)

        if not next_move:
            self.moves_pos.append(possible_moves)
            if not possible_moves:
                self.captured_num = -1

        for move in capture_moves:
            x = move[0]
            y = move[1]

            if self.row + x + x < 0 or self.row + x + x >= 8 \
                    or self.col + y + y < 0 or self.col + y + y >= 8:
                continue

            if self.row + x < 0 or self.row + x >= 8 \
                    or self.col + y < 0 or self.col + y >= 8:
                continue

            if board[self.row+x, self.col+y] is None:
                continue

            if board[self.row+x, self.col+y].color == self.color:
                continue

            if board[self.row + x + x, self.col + y + y] is None:
                next_move = True
                self.next_moves(
                    board, self.row + x + x, self.col + y + y,
                    [(self.row + x + x, self.col + y + y)],
                    [(self.row + x, self.col + y)], move, 1)

    def next_moves(self, board, row, col, possible_moves,
                   captured_pos, previous_pos, captures_num):
        previous_pos = tuple(map(lambda x: x*-1, previous_pos))
        moves = [(i, j) for j in (-1, 1) for i in (-1, 1) if (i, j) != previous_pos]
        recursion = False

        for move in moves:
            x, y = move

            if row+x < 0 or row+x >= 8 \
                    or col+y < 0 or col+y >= 8:
                continue

            if row+x+x < 0 or row+x+x >= 8 \
                    or col+y+y < 0 or col+y+y >= 8:
                continue

            if board[row+x, col+y] is None:
                continue

            if board[row + x, col + y].color == self.color:
                continue

            if board[row + x + x, col + y + y] is None:
                new_moves = copy.deepcopy(possible_moves)
                new_captures = copy.deepcopy(captured_pos)
                new_moves.append((row+x+x, col+y+y))
                new_captures.append((row+x, col+y))
                recursion = True
                self.next_moves(
                    board, row + x + x, col + y + y, new_moves,
                    new_captures, move, captures_num+1)

        if not recursion:
            if captures_num > self.captured_num:
                self.captured_num = captures_num
                self.moves_pos = [possible_moves, ]
                self.captured_pieces = [captured_pos, ]
            elif captures_num == self.captured_num:
                self.moves_pos.append(possible_moves)
                self.captured_pieces.append(captured_pos)


class King(Piece):
    moves = ((1, -1), (1, 1), (-1, -1), (-1, 1))

    def __init__(self, color, row, col, number):
        super().__init__(color, row, col, number)

    def first_move(self, board):
        self.captured_num = -1
        self.moves_pos = []
        self.captured_pieces = []
        all_possible_moves = []
        next_move = False

        for move in self.moves:
            x, y = move
            row = self.row
            col = self.col
            possible_moves = []

            i = 1
            while True:
                if row + i*x < 0 or row + i*x >= 8 \
                        or col + i*y < 0 or col + i*y >= 8:
                    break

                if board[row + i*x, col + i*y] is None:
                    if not next_move:
                        possible_moves.append((row + i*x, col + i*y))
                else:
                    if board[row + i*x, col + i*y].color == self.color:
                        break

                    if row + i*x + x < 0 or row + i*x + x >= 8 \
                            or col + i*y + y < 0 or col + i*y + y >= 8:
                        break

                    if board[row + i*x + x, col + i*y + y] is not None:
                        break

                    j = i
                    while True:
                        if row + j*x + x < 0 or row + j*x + x >= 8 \
                                or col + j*y + y < 0 or col + j*y + y >= 8:
                            break

                        if board[row + j*x + x, col + j*y + y] is not None:
                            break

                        next_move = True
                        self.next_moves(
                            board, row + j*x + x, col + j*y + y,
                            [(row + j*x + x, col + j*y + y)],
                            [(row + i*x, col + i*y)], move, 1)
                        j += 1
                i += 1

            if possible_moves:
                all_possible_moves.append(possible_moves)

        if not next_move:
            self.moves_pos = all_possible_moves
            self.captured_num = 0
            if not all_possible_moves:
                self.captured_num = -1

    def next_moves(self, board, row, col, possible_moves,
                   captured_pos, previous_pos, captures_num):
        previous_pos = tuple(map(lambda x: x*-1, previous_pos))
        moves = [(i, j) for j in (-1, 1) for i in (-1, 1) if (i, j) != previous_pos]
        recursion = False

        for move in moves:
            x, y = move

            i = 1
            while True:
                if row + i*x < 0 or row + i*x >= 8 \
                        or col + i * y < 0 or col + i * y >= 8:
                    break

                if board[row + i*x, col + i*y] is None:
                    i += 1
                    continue

                if board[row + i*x, col + i*y].color == self.color:
                    break

                if row + i*x + x < 0 or row + i*x + x >= 8 \
                        or col + i*y + y < 0 or col + i*y + y >= 8:
                    break

                if board[row + i*x + x, col + i*y + y] is not None:
                    break

                j = i
                while True:
                    if row + j*x + x < 0 or row + j*x + x >= 8 \
                            or col + j*y + y < 0 or col + j*y + y >= 8:
                        break

                    if board[row + j*x + x, col + j*y + y] is not None:
                        break

                    recursion = True
                    new_moves = copy.deepcopy(possible_moves)
                    new_captures = copy.deepcopy(captured_pos)
                    new_moves.append((row + j*x + x, col + j*y + y))
                    new_captures.append((row + i*x, col + i*y))

                    self.next_moves(
                        board, row + j*x + x, col + j*y + y,
                        new_moves, new_captures, move, captures_num+1)

                    j += 1
                i += 1

        if not recursion:
            if captures_num > self.captured_num:
                self.captured_num = captures_num
                self.moves_pos = [possible_moves, ]
                self.captured_pieces = [captured_pos, ]
            elif captures_num == self.captured_num:
                self.moves_pos.append(possible_moves)
                self.captured_pieces.append(captured_pos)