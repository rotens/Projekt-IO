import copy
import tkinter as tk


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


class GameInterface(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.board_canvas = None
        self.bottom_frame = None
        self.pieces = []
        self.piece_selection = None
        self.field_selections = []
        self.board = None
        self.pack()
        self._draw_window()
        self._draw_pieces()

    def _draw_window(self):
        self['bg'] = LIGHT_FIELD
        self.board_canvas = tk.Canvas(
            master=self, width=CANVAS_HEIGHT_PX, height=CANVAS_WIDTH_PX,
            background=DARK_FIELD, borderwidth=0, highlightthickness=0)
        self.board_canvas.pack()

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

        self.bottom_frame = tk.Frame(
            master=self, width=CANVAS_WIDTH_PX, height=BOTTOM_FRAME_HEIGHT_PX,
            bg=DARK_FIELD)
        self.bottom_frame.pack()

        self.btn_start_game = tk.Button(
            master=self.bottom_frame, text="Rozpocznij grę", bg=BUTTON,
            fg=WHITE, font=("", BUTTON_TEXT_SIZE_PX), command=self.start_game)
        self.btn_start_game.place(x=110, y=8)

        self.dark_counter = tk.Label(
            master=self.bottom_frame, text="12", font=("", COUNTER_SIZE_PX),
            fg=BLACK, bg=DARK_FIELD)
        self.dark_counter.place(x=440, y=5)

        self.light_counter = tk.Label(
            master=self.bottom_frame, text="12", font=("", COUNTER_SIZE_PX),
            fg=WHITE, bg=DARK_FIELD)
        self.light_counter.place(x=380, y=5)

        self.game_info_text = tk.Label(
            master=self.bottom_frame, text="Teraz kolej",
            font=("", COUNTER_SIZE_PX), fg=LIGHT_FIELD, bg=DARK_FIELD)
        self.game_info_text.place(x=550, y=5)
        self.game_info_color = tk.Label(
            master=self.bottom_frame, text="",
            font=("", COUNTER_SIZE_PX), fg=WHITE, bg=DARK_FIELD)
        self.game_info_color.place(x=715, y=5)

    def _draw_pieces(self):
        if self.pieces:
            for piece in self.pieces:
                self.board_canvas.delete(piece)
            self.pieces = []

        for row in range(3):
            for col in range(8):
                if col % 2 == ((row + 1) % 2):
                    piece_id = self.board_canvas.create_oval(
                        BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 19,
                        BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 19,
                        BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 80,
                        BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 80,
                        fill=BLACK, outline=BLACK)
                    self.pieces.append(str(piece_id))

            for col in range(8):
                row2 = 7 - row
                if col % 2 == ((row2 + 1) % 2):
                    piece_id = self.board_canvas.create_oval(
                        BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 19,
                        BOARD_TOP_LEFT_PX + row2 * FIELD_SIZE + 19,
                        BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 80,
                        BOARD_TOP_LEFT_PX + row2 * FIELD_SIZE + 80,
                        fill=WHITE, outline=WHITE)
                    self.pieces.append(str(piece_id))

    def select(self, event):
        if event.x < 50 or event.x > 849:
            return
        if event.y < 50 or event.y > 849:
            return

        row = (event.y - 50) // 100
        col = (event.x - 50) // 100

        if self.board[row, col] is not None:
            if self.board[row, col].blocked:
                return

            if self.board.active:
                if not self.board[row, col].active:
                    self.board.deactivate_current_piece()
                    self.remove_piece_selection()
                    self.remove_field_selection()

            #self.remove_piece_selection()
            self.board.active = True
            self.board[row, col].active = True
            self.board.active_piece = (row, col)
            self.draw_piece_selection(row, col)
            self.selection_process(row, col)
            print("Move {}".format(self.board[row, col].moves_pos))
            print("Capture {}".format(self.board[row, col].captured_pieces))

        else:
            self.move_process(row, col)

    def selection_process(self, row, col):
        if self.board.max_moves == 0:
            self.board.active_fields = self.board[row, col].moves_pos
            self.draw_field_selection()
        else:
            index = self.board[row, col].captured_num - self.board.max_moves
            self.board.active_fields = []

            if not self.board.indices:
                for move in self.board[row, col].moves_pos:
                    self.board.active_fields.append([move[index]])
            else:
                for i in self.board.indices:
                    field_pos = self.board[row, col].moves_pos[i][index]
                    self.board.active_fields.append([field_pos])

            self.draw_field_selection()

    def move_process(self, row, col):
        if not self.board.active:
            return

        if self.board.max_moves == 0:
            x, y = self.board.active_piece

            for lst in self.board[x, y].moves_pos:
                if (row, col) in lst:
                    self.remove_piece_selection()
                    self.remove_field_selection()
                    self.board.active_fields = []
                    self.field_selections = []
                    self.board.active = False
                    self.board.deactivate_current_piece()

                    index = self.board[x, y].number
                    self.move_piece(self.pieces[index], self.board.active_piece, row, col)
                    self.board.move_piece(row, col)

                    self.board.active_piece = ()
                    self.board.change_color()
                    self.pieces_left()
                    self.game_state()
                    #self.board.print_board()

        else:
            x, y = self.board.active_piece
            index = self.board[x, y].captured_num - self.board.max_moves

            if not self.board.indices:
                for i, lst in enumerate(self.board[x, y].moves_pos):
                    if lst[index] == (row, col):
                        self.board.indices.append(i)
            else:
                temp_indices = []
                for i in self.board.indices:
                    if self.board[x, y].moves_pos[i] == (row, col):
                        temp_indices.append(i)
                self.board.indices = temp_indices

            if self.board.indices:
                self.remove_piece_selection()
                self.remove_field_selection()
                self.board.active_fields = []
                self.field_selections = []
                self.board.active = False
                self.board.deactivate_current_piece()

                # Moving piece
                piece_index = self.board[x, y].number
                self.move_piece(self.pieces[piece_index], self.board.active_piece, row, col)
                self.board.move_piece(row, col)

                # Capturing piece
                captured_row, captured_col = self.board[row, col].captured_pieces[self.board.indices[0]][index]
                piece_id = self.pieces[self.board[captured_row, captured_col].number]
                self.board.capture(captured_row, captured_col)
                self.remove_piece(piece_id)

                self.board.block_other_pieces(piece_index)
                self.board.max_moves -= 1
                self.pieces_left()

            if self.board.max_moves == 0:
                self.board.active_piece = ()
                self.board.indices = []
                self.board.change_color()
                #self.pieces_left()
                self.game_state()

    def draw_piece_selection(self, row, col):
        self.piece_selection = self.board_canvas.create_oval(
            BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 25,
            BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 25,
            BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 74,
            BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 74,
            outline=RED, width=3)

    def remove_piece_selection(self):
        self.board_canvas.delete(self.piece_selection)

    def draw_field_selection(self):
        for lst in self.board.active_fields:
            for pos in lst:
                row, col = pos
                self.field_selections.append(
                    self.board_canvas.create_rectangle(
                        BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 10,
                        BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 10,
                        BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 89,
                        BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 89,
                        outline=WHITE, width=3))

    def remove_field_selection(self):
        for selection in self.field_selections:
            self.board_canvas.delete(selection)

    def bind_event(self):
        self.board_canvas.bind('<ButtonPress-1>', self.select)

    def unbind_event(self):
        self.board_canvas.unbind('<ButtonPress-1>')

    def move_piece(self, piece_id, active_piece, target_row, target_col):
        x = (target_row - active_piece[0]) * 100
        y = (target_col - active_piece[1]) * 100
        self.board_canvas.move(piece_id, y, x)

        row, col = active_piece
        if isinstance(self.board[row, col], King):
            self.board_canvas.move("T{}".format(piece_id), y, x)

    def remove_piece(self, piece_id):
        self.board_canvas.delete(piece_id)

        #if isinstance(self.board[row, col], King):
        self.board_canvas.delete("T{}".format(piece_id))

    def create_king(self, row, col):
        number = self.board[row, col].number
        piece_id = self.pieces[number]
        color = WHITE if self.board[row, col].color == "dark" else BLACK

        self.board_canvas.create_text(
            BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 50,
            BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 50,
            text="D", font=("", NOTATION_FONT_SIZE_PX),
            fill=color, tags="T{}".format(piece_id))

    def start_game(self):
        self.remove_piece_selection()
        self.remove_field_selection()
        self.piece_selection = None
        self.field_selections = []
        self.board = Board()
        self._draw_pieces()

        self.create_king(5, 6)

        self.bind_event()
        self.pieces_left()
        self.game_state()

    def game_state(self):
        value = self.board.game_state()

        if value == 1:
            self.unbind_event()
            self.game_info_text["text"] = "Wygrały"
            self.game_info_color["text"] = "białe!"

        elif value == 2:
            self.unbind_event()
            self.game_info_text["text"] = "Wygrały"
            self.game_info_color["text"] = "czarne!"

        elif value == 3:
            self.unbind_event()
            self.game_info_text["text"] = "Remis!"
            self.game_info_color["text"] = ""

        else:
            self.game_info()

    def game_info(self):
        if self.board.current_color == "light":
            self.game_info_color["text"] = "białych"
            self.game_info_color["fg"] = WHITE
        else:
            self.game_info_color["text"] = "czarnych"
            self.game_info_color["fg"] = BLACK

    def pieces_left(self):
        self.light_counter["text"] = self.board.light_left
        self.dark_counter["text"] = self.board.dark_left


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
        self.make_king(5, 6)
        self.possible_captures()
        print(self.board[5][6].captured_num)

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

        #self.board[5][4] = King("light", 5, 4, 22)
        #self.print_board()

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
            if not all_possible_moves:
                print("King")
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


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    GameInterface(root)
    root.mainloop()
