import copy

from pieces import Man, King


ROWS = 8
COLS = 8


class Board:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.active = False
        self.active_piece = []
        self.active_fields = []
        self.light_pieces = []
        self.dark_pieces = []
        self.indices = []
        self.max_moves = 0
        self.current_color = ""
        self.light_left = 0
        self.dark_left = 0
        self.no_capture_light = 0
        self.no_capture_dark = 0
        self.init_board()

    def __getitem__(self, pos):
        return self.board[pos[0]][pos[1]]

    def init_board(self):
        self.active = False
        self.active_piece = []
        self.active_fields = []
        self.light_pieces = []
        self.dark_pieces = []
        self.indices = []
        self.max_moves = 0
        self.current_color = "light"
        self.light_left = 12
        self.dark_left = 12
        self.no_capture_light = 15
        self.no_capture_dark = 15
        self.create_board()
        self.possible_captures()

    def create_board(self):
        counter = 0
        for row in range(3):
            for col in range(8):
                if col % 2 == ((row + 1) % 2):
                    self.board[row][col] = Man("dark", row, col, counter)
                    self.dark_pieces.append(self.board[row][col])
                    counter = counter + 1
            for col in range(8):
                row2 = 7 - row
                if col % 2 == ((row2 + 1) % 2):
                    self.board[row2][col] = Man("light", row2, col, counter)
                    self.light_pieces.append(self.board[row2][col])
                    counter = counter + 1

    def deactivate_current_piece(self):
        row = self.active_piece[0]
        col = self.active_piece[1]
        self.board[row][col].active = False

    def activate_piece(self, row, col):
        self.board[row][col].active = True

    def move_piece(self, target_row, target_col):
        row = self.active_piece[0]
        col = self.active_piece[1]
        self.board[row][col].move(target_row, target_col)
        self.board[target_row][target_col] = copy.deepcopy(self.board[row][col])
        self.board[row][col] = None

        if self.current_color == "light":
            pieces = self.light_pieces
        else:
            pieces = self.dark_pieces

        for i, _ in enumerate(pieces):
            if pieces[i].number == self.board[target_row][target_col].number:
                pieces[i] = self.board[target_row][target_col]

    def unblock_pieces(self):
        if self.current_color == "light":
            pieces = self.light_pieces
        else:
            pieces = self.dark_pieces

        for piece in pieces:
            piece.blocked = False

    def block_pieces(self):
        if self.current_color == "light":
            current_pieces = self.light_pieces
            opposite_pieces = self.dark_pieces
        else:
            current_pieces = self.dark_pieces
            opposite_pieces = self.light_pieces

        for piece in opposite_pieces:
            piece.blocked = True

        for piece in current_pieces:
            if piece.captured_num < self.max_moves:
                piece.blocked = True

    def block_other_pieces(self, number):
        if self.current_color == "light":
            pieces = self.light_pieces
        else:
            pieces = self.dark_pieces

        for piece in pieces:
            if piece.number != number:
                piece.blocked = True

    def possible_captures(self):
        pieces = self.light_pieces if self.current_color == "light" else self.dark_pieces
        self.max_moves = -1

        for piece in pieces:
            piece.first_move(self)

            if piece.captured_num > self.max_moves:
                self.max_moves = piece.captured_num

        self.block_pieces()

    def change_color(self):
        if self.current_color == "light":
            self.current_color = "dark"
        else:
            self.current_color = "light"

        self.unblock_pieces()
        self.possible_captures()

    def make_king(self, row, col):
        number = self.board[row][col].number
        color = self.board[row][col].color
        self.board[row][col] = King(color, row, col, number)

        pieces = self.light_pieces if color == "light" else self.dark_pieces

        for i, piece in enumerate(pieces):
            if piece.number == number:
                pieces[i] = self.board[row][col]
                break

    def capture(self, row, col):
        number = self.board[row][col].number
        self.board[row][col] = None

        if self.current_color == "light":
            pieces = self.dark_pieces
            self.dark_left -= 1
        else:
            pieces = self.light_pieces
            self.light_left -= 1

        for i, piece in enumerate(pieces):
            if piece.number == number:
                pieces.pop(i)
                break

    def game_state(self):
        if self.dark_left == 0:
            return 1

        if self.light_left == 0:
            return 2

        if not self.no_capture_dark and not self.no_capture_light:
            return 3

        if self.max_moves == -1:
            if self.current_color == 'light':
                return 2
            else:
                return 1

        return 0
