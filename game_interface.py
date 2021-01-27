import tkinter as tk

from board import Board
from pieces import Man, King


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

INFO_WHITE = "białych"
INFO_BLACK = "czarnych"
INFO_BLACK_WIN = "czarne!"
INFO_WHITE_WIN = "białe!"
INFO_TEXT = "Teraz kolej"
INFO_TEXT_WIN = "Wygrały"
INFO_DRAW = "Remis!"


class GameInterface(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.board_canvas = None
        self.bottom_frame = None
        self.pieces = []
        self.piece_selection = None
        self.field_selections = []
        self.king_symbols = []
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
            master=self.bottom_frame, text=INFO_TEXT,
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
                if (row, col) == self.board.active_piece:
                    return

                if not self.board[row, col].active:
                    self.board.deactivate_current_piece()
                    self.remove_piece_selection()
                    self.remove_field_selection()

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
                    #self.field_selections = []
                    self.board.active = False
                    self.board.deactivate_current_piece()

                    index = self.board[x, y].number
                    self.move_piece(self.pieces[index], self.board.active_piece, row, col)
                    self.board.move_piece(row, col)

                    if self.board.current_color == "light":
                        self.board.no_capture_light -= 1
                    else:
                        self.board.no_capture_dark -= 1

                    if row == 0 or row == 7:
                        if isinstance(self.board[row, col], Man):
                            self.board.make_king(row, col)
                            self.create_king(row, col)

                    self.board.active_piece = ()
                    self.board.change_color()
                    self.pieces_left()
                    self.game_state()

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
                #self.field_selections = []
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
                if row == 0 or row == 7:
                    if isinstance(self.board[row, col], Man):
                        self.board.make_king(row, col)
                        self.create_king(row, col)

                self.board.active_piece = ()
                self.board.indices = []
                self.board.change_color()
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
        self.field_selections = []

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
        self.board_canvas.delete("T{}".format(piece_id))

    def remove_symbols(self):
        for tag in self.king_symbols:
            self.board_canvas.delete(tag)
        self.king_symbols = []

    def create_king(self, row, col):
        number = self.board[row, col].number
        piece_id = self.pieces[number]
        color = WHITE if self.board[row, col].color == "dark" else BLACK

        self.board_canvas.create_text(
            BOARD_TOP_LEFT_PX + col * FIELD_SIZE + 50,
            BOARD_TOP_LEFT_PX + row * FIELD_SIZE + 50,
            text="D", font=("", NOTATION_FONT_SIZE_PX),
            fill=color, tags="T{}".format(piece_id))

        self.king_symbols.append("T{}".format(piece_id))

    def start_game(self):
        self.remove_symbols()
        self.remove_piece_selection()
        self.remove_field_selection()
        self.piece_selection = None
        #self.field_selections = []
        self.board = Board()
        self._draw_pieces()
        self.bind_event()
        self.pieces_left()
        self.game_info_text['text'] = INFO_TEXT
        self.game_info_color.place(x=715)
        self.game_info_text.place(x=550)
        self.game_state()

    def game_state(self):
        value = self.board.game_state()

        if value == 1:
            self.unbind_event()
            self.game_info_text["text"] = INFO_TEXT_WIN
            self.game_info_color["text"] = INFO_WHITE_WIN
            self.game_info_color.place(x=675)

        elif value == 2:
            self.unbind_event()
            self.game_info_text["text"] = INFO_TEXT_WIN
            self.game_info_color["text"] = INFO_BLACK_WIN
            self.game_info_color.place(x=675)

        elif value == 3:
            self.unbind_event()
            self.game_info_text["text"] = INFO_DRAW
            self.game_info_color["text"] = ""
            self.game_info_text.place(x=650)
            self.game_info_color.place(x=800)

        else:
            self.game_info()

    def game_info(self):
        if self.board.current_color == "light":
            self.game_info_color["text"] = INFO_WHITE
            self.game_info_color["fg"] = WHITE
        else:
            self.game_info_color["text"] = INFO_BLACK
            self.game_info_color["fg"] = BLACK

    def pieces_left(self):
        self.light_counter["text"] = self.board.light_left
        self.dark_counter["text"] = self.board.dark_left
