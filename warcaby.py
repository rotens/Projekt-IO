import copy
import tkinter as tk


# Colors
LIGHT_FIELD = "#B2AB98"
DARK_FIELD = "#523934"
WHITE = "#FFFFFF"
BLACK = "#000000"
RED = "#FF0000"
BUTTON = "#504D4D"

NOTATION_LETTERS = "ABCDEFGH"

FIELD_SIZE = 100
NOTATION_FONT_SIZE_PX = 32
CANVAS_HEIGHT_PX = 900
CANVAS_WIDTH_PX = 900
BOARD_TOP_LEFT_PX = 50
BOTTOM_FRAME_HEIGHT_PX = 55
BUTTON_TEXT_SIZE_PX = 16
COUNTER_SIZE_PX = 25

ROWS = 8
COLS = 8


class GUI(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.board_canvas = None
        self.bottom_frame = None
        self.pieces = []
        self.piece_selection = None
        self.field_selections = []
        self.board = Board()
        self.pack()
        self._draw_window()
        self._draw_pieces()

    def _draw_window(self):
        self['bg'] = LIGHT_FIELD

        self.board_canvas = tk.Canvas(
            master=self, width=CANVAS_HEIGHT_PX, height=CANVAS_WIDTH_PX,
            background=DARK_FIELD, borderwidth=0, highlightthickness=0)
        self.board_canvas.bind('<ButtonPress-1>', self.select)
        self.board_canvas.pack()
        self.bind_event()
        self.board_canvas.create_rectangle(49, 49, 850, 850)

        for i in range(8):
            if i % 2 == 1:
                for j in range(1, 8, 2):
                    self.board_canvas.create_rectangle(
                        j*100 + BOARD_TOP_LEFT_PX, i*100 + BOARD_TOP_LEFT_PX,
                        j*100 + 99 + BOARD_TOP_LEFT_PX, i*100 + 99 + BOARD_TOP_LEFT_PX,
                        fill=LIGHT_FIELD, outline=LIGHT_FIELD)
            else:
                for j in range(0, 8, 2):
                    self.board_canvas.create_rectangle(
                        j * 100 + BOARD_TOP_LEFT_PX, i * 100 + BOARD_TOP_LEFT_PX,
                        j * 100 + 99 + BOARD_TOP_LEFT_PX, i * 100 + 99 + BOARD_TOP_LEFT_PX,
                        fill=LIGHT_FIELD, outline=LIGHT_FIELD)

        for i in range(8):
            self.board_canvas.create_text(
                i * 100 + BOARD_TOP_LEFT_PX + 50, 874, text=(NOTATION_LETTERS[i]), anchor=tk.CENTER,
                font=('TkMenuFont', NOTATION_FONT_SIZE_PX), fill=LIGHT_FIELD)
            self.board_canvas.create_text(
                i * 100 + BOARD_TOP_LEFT_PX + 50, 24, text=(NOTATION_LETTERS[8-i-1]), anchor=tk.CENTER,
                font=('TkMenuFont', NOTATION_FONT_SIZE_PX), fill=LIGHT_FIELD, angle=180)
            self.board_canvas.create_text(
                874, i * 100 + BOARD_TOP_LEFT_PX + 50, text=i+1, anchor=tk.CENTER,
                font=('TkMenuFont', NOTATION_FONT_SIZE_PX), fill=LIGHT_FIELD, angle=180)
            self.board_canvas.create_text(
                24, i * 100 + BOARD_TOP_LEFT_PX + 50, text=8-i, anchor=tk.CENTER,
                font=('TkMenuFont', NOTATION_FONT_SIZE_PX), fill=LIGHT_FIELD)

        self.board_canvas.create_rectangle(0, CANVAS_HEIGHT_PX-1, CANVAS_WIDTH_PX-1, CANVAS_HEIGHT_PX-1)

        self.bottom_frame = tk.Frame(master=self, width=CANVAS_WIDTH_PX, height=BOTTOM_FRAME_HEIGHT_PX, bg=DARK_FIELD)
        self.bottom_frame.pack()

        self.btn_start_game = tk.Button(
            master=self.bottom_frame, text="Rozpocznij grę", bg=BUTTON,
            fg=WHITE, font=("", BUTTON_TEXT_SIZE_PX))
        self.btn_start_game.place(x=110, y=8)

        self.dark_counter = tk.Label(
            master=self.bottom_frame, text="20", font=("", COUNTER_SIZE_PX), fg=BLACK, bg=DARK_FIELD)
        self.dark_counter.place(x=440, y=5)

        self.light_counter = tk.Label(
            master=self.bottom_frame, text="20", font=("", COUNTER_SIZE_PX), fg=WHITE, bg=DARK_FIELD)
        self.light_counter.place(x=380, y=5)

        self.game_info_text = tk.Label(
            master=self.bottom_frame, text="Teraz kolej",
            font=("", COUNTER_SIZE_PX), fg=LIGHT_FIELD, bg=DARK_FIELD)
        self.game_info_text.place(x=550, y=5)
        self.game_info_color = tk.Label(
            master=self.bottom_frame, text="białych",
            font=("", COUNTER_SIZE_PX), fg=WHITE, bg=DARK_FIELD)
        self.game_info_color.place(x=715, y=5)

    def _draw_pieces(self):
        if self.pieces:
            for piece in self.pieces:
                self.board_canvas.delete(piece)

        for row in range(3):
            for col in range(8):
                if col % 2 == ((row + 1) % 2):
                    piece_id = self.board_canvas.create_oval(
                        BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 19,  BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 19,
                        BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 80, BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 80,
                        fill=BLACK, outline=BLACK)
                    self.pieces.append(piece_id)
            for col in range(8):
                row2 = 7 - row
                if col % 2 == ((row2 + 1) % 2):
                    piece_id = self.board_canvas.create_oval(
                        BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 19, BOARD_TOP_LEFT_PX + row2 * FIELD_SIZE + 19,
                        BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 80, BOARD_TOP_LEFT_PX + row2 * FIELD_SIZE + 80,
                        fill=WHITE, outline=WHITE)
                    self.pieces.append(piece_id)

        #print(self.pieces)

        # self.board_canvas.create_oval(
        #     100+BOARD_TOP_LEFT_PX + 25, BOARD_TOP_LEFT_PX + 25,
        #     100+BOARD_TOP_LEFT_PX + 74,  BOARD_TOP_LEFT_PX + 74,
        #     outline=RED, width=3)

    def select(self, event):
        #print(type(event))
        if event.x < 50 or event.x > 849:
            return
        if event.y < 50 or event.y > 849:
            return

        row = (event.y - 50) // 100
        col = (event.x - 50) // 100

        #print(self.board.active)

        if self.board.active:
            if self.board[row, col] is not None:
                if not self.board[row, col].active:
                    self.board.deactivate_current_piece()
                    self.remove_piece_selection()
                    self.board[row, col].active = True
                    self.board.active_piece = (row, col)
                    self.draw_piece_selection(row, col)
                    self.board[row, col].first_move(self.board)
                    print("Move {}".format(self.board[row, col].moves_pos))
                    print("Capture {}".format(self.board[row, col].captured_pieces))

            else:
                self.remove_piece_selection()
                self.board.active = False
                self.board.move_piece(row, col)
                index = self.board[row, col].number
                self.move_piece(self.pieces[index], self.board.active_piece, row, col)

        else:
            if self.board[row, col] is not None:
                self.board[row, col].active = True
                self.board.active_piece = (row, col)
                self.draw_piece_selection(row, col)
                self.board.active = True
                self.board[row, col].first_move(self.board)
                print("Move {}".format(self.board[row, col].moves_pos))
                print("Capture {}".format(self.board[row, col].captured_pieces))

        #print("{}, {}".format(row, col))

    def draw_piece_selection(self, row, col):
        self.piece_selection = self.board_canvas.create_oval(
            BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 25,
            BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 25,
            BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 74,
            BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 74,
            outline=RED, width=3)

    def remove_piece_selection(self):
        self.board_canvas.delete(self.piece_selection)

    def draw_field_selection(self, possible_moves, row, col):
        pass

    def remove_field_selection(self):
        pass

    def bind_event(self):
        self.board_canvas.bind('<ButtonPress-1>', self.select)

    def unbind_event(self):
        self.board_canvas.unbind()

    def move_piece(self, piece_id, active_piece, target_row, target_col):
        x = (target_row - active_piece[0]) * 100
        y = (target_col - active_piece[1]) * 100
        self.board_canvas.move(piece_id, y, x)

    def create_king(self):
        pass


class Board:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.active = False
        self.active_piece = ()
        self.active_fields = ()
        self.light_pieces = []
        self.dark_pieces = []
        self.max_moves = 0
        self.current_color = "light"
        self.create_board()

    def __getitem__(self, pos):
        return self.board[pos[0]][pos[1]]

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

        self.board[5][4] = King("light", 5, 4, 23)
        #self.print_board()
        # print(self.light_pieces)
        # print(self.dark_pieces)

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

    def block_pieces(self):
        pieces = self.light_pieces if self.current_color == "light" else self.dark_pieces

        for piece in pieces:
            piece.blocked = True

    def possible_captures(self):
        pieces = self.light_pieces if self.current_color == "light" else self.dark_pieces

        for piece in pieces:
            piece.get_valid_fields(self.board, first_move=True)

    def print_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is not None:
                    if self.board[row][col].color == "light":
                        print("l", end="")
                    else:
                        print("d", end="")
                else:
                    print("0", end="")
            print()


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

    def get_valid_fields(self, board):
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
                self.next_moves(
                    board, self.row + x + x, self.col + y + y,
                    [(self.row + x + x, self.col + y + y)],
                    [(self.row + x, self.col + y)], move, 1)

    def next_moves(self, board, row, col, possible_moves,
                   captured_pos, previous_pos, captures_num):
        # possible_moves = copy.deepcopy(possible_moves)
        # captured_pos = copy.deepcopy(captured_pos)
        previous_pos = (previous_pos[0]*-1, previous_pos[1]*-1)
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
        self.captured_num = 0
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

                    j = i
                    while True:
                        if row + j * x + x < 0 or row + j * x + x >= 8 \
                                or col + i * y + y < 0 or col + i * y + y >= 8:
                            break

                        if board[row + j*x + x, col + j*y + y] is not None:
                            break

                        next_move = True
                        self.next_moves(
                            board, row + j*x + x, col + j*y + y,
                            [(row + j*x + x, col + j*y + y)],
                            [(row + j*x, col + j*y)], move, 1)
                        j += 1
                i += 1

            if possible_moves:
                all_possible_moves.append(possible_moves)

        if not next_move:
            self.moves_pos = all_possible_moves

    def next_moves(self, board, row, col, possible_moves,
                   captured_pos, previous_pos, captures_num):
        #previous_pos = (previous_pos[0] * -1, previous_pos[1] * -1)
        previous_pos = tuple(map(lambda x: x*-1, previous_pos))
        moves = [(i, j) for j in (-1, 1) for i in (-1, 1) if (i, j) != previous_pos]
        recursion = False

        for move in moves:
            x, y = move


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    GUI(root)
    root.mainloop()
