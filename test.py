import tkinter as tk
import unittest


from board import Board
from game_interface import GameInterface
from pieces import King


class TestBoard(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = Board()
        self.board2 = Board()
        self.board3 = None
        self.board4 = None

    def test_current_color(self):
        self.assertEqual(self.board.current_color, "light")
        self.board.change_color()
        self.assertEqual(self.board.current_color, "dark")
        self.board.change_color()
        self.assertEqual(self.board.current_color, "light")

    def test_light_win(self):
        self.board.dark_left = 0
        self.assertEqual(self.board.game_state(), 1)

    def test_light_win2(self):
        self.board.max_moves = -1
        self.board.current_color = "dark"
        self.assertEqual(self.board.game_state(), 1)

    def test_dark_win(self):
        self.board.light_left = 0
        self.assertEqual(self.board.game_state(), 2)

    def test_dark_win2(self):
        self.board.max_moves = -1
        self.board.current_color = "light"
        self.assertEqual(self.board.game_state(), 2)

    def test_draw(self):
        self.board.no_capture_dark = 0
        self.board.no_capture_light = 0
        self.assertEqual(self.board.game_state(), 3)

    def test_normal_state(self):
        self.board.light_left = 12
        self.board.dark_left = 12
        self.board.max_moves = 0
        self.board.no_capture_dark = 15
        self.board.no_capture_light = 15
        self.assertEqual(self.board.game_state(), 0)

    def test_unblock_light_pieces(self):
        for piece in self.board.light_pieces:
            piece.blocked = True

        self.board.current_color = "light"
        self.board.unblock_pieces()

        for piece in self.board.light_pieces:
            self.assertFalse(piece.blocked)

    def test_unblock_dark_pieces(self):
        for piece in self.board.dark_pieces:
            piece.blocked = True

        self.board.current_color = "dark"
        self.board.unblock_pieces()

        for piece in self.board.dark_pieces:
            self.assertFalse(piece.blocked)

    def test_block_light_pieces(self):
        for piece in self.board.light_pieces:
            piece.blocked = False

        self.board.current_color = "dark"
        self.board.block_pieces()

        for piece in self.board.light_pieces:
            self.assertTrue(piece.blocked)

    def test_block_dark_pieces(self):
        for piece in self.board.dark_pieces:
            piece.blocked = False

        self.board.current_color = "light"
        self.board.block_pieces()

        for piece in self.board.dark_pieces:
            self.assertTrue(piece.blocked)

    def test_block_other_light_pieces(self):
        for piece in self.board.light_pieces:
            piece.blocked = False

        self.board.current_color = "light"
        self.board.block_other_pieces(23)

        for piece in self.board.light_pieces:
            if piece.number == 23:
                self.assertFalse(piece.blocked)
            else:
                self.assertTrue(piece.blocked)

    def test_block_other_dark_pieces(self):
        for piece in self.board.dark_pieces:
            piece.blocked = False

        self.board.current_color = "dark"
        self.board.block_other_pieces(0)

        for piece in self.board.dark_pieces:
            if piece.number == 0:
                self.assertFalse(piece.blocked)
            else:
                self.assertTrue(piece.blocked)

    def test_possible_moves(self):
        values = [
            [(5, 6), [[(4, 5), (4, 7)]]],
            [(5, 4), [[(4, 3), (4, 5)]]],
            [(5, 2), [[(4, 1), (4, 3)]]],
            [(5, 0), [[(4, 1)]]],
            [(6, 1), []],
            [(6, 3), []],
            [(6, 5), []],
            [(6, 7), []],
            [(7, 0), []],
            [(7, 2), []],
            [(7, 4), []],
            [(7, 6), []],
        ]

        for lst in values:
            row, col = lst[0]
            self.assertEqual(self.board[row, col].moves_pos, lst[1])

    def test_possible_captures(self):
        for piece in self.board.light_pieces:
            self.assertEqual(piece.captured_pieces, [])

    def test_possible_moves2(self):
        self.board2.change_color()

        values = [
            [(2, 7), [[(3, 6)]]],
            [(2, 5), [[(3, 4), (3, 6)]]],
            [(2, 3), [[(3, 2), (3, 4)]]],
            [(2, 1), [[(3, 0), (3, 2)]]],
            [(1, 6), []],
            [(1, 4), []],
            [(1, 2), []],
            [(1, 0), []],
            [(0, 7), []],
            [(0, 5), []],
            [(0, 3), []],
            [(0, 1), []],
        ]

        for lst in values:
            row, col = lst[0]
            self.assertEqual(self.board2[row, col].moves_pos, lst[1])

    def test_possible_captures2(self):
        for piece in self.board.dark_pieces:
            self.assertEqual(piece.captured_pieces, [])

    def test_possible_moves3(self):
        self.board3 = Board()
        self.board3.active_piece = (5, 6)
        self.board3.move_piece(4, 5)
        self.board3.active_piece = (5, 4)
        self.board3.move_piece(4, 3)
        self.board3.change_color()
        self.board3.active_piece = (2, 1)
        self.board3.move_piece(3, 2)
        self.board3.possible_captures()

        self.assertEqual(self.board3[3, 2].moves_pos, [[(5, 4), (3, 6)]])

    def test_possible_captures3(self):
        self.board3 = Board()
        self.board3.active_piece = (5, 6)
        self.board3.move_piece(4, 5)
        self.board3.active_piece = (5, 4)
        self.board3.move_piece(4, 3)
        self.board3.change_color()
        self.board3.active_piece = (2, 1)
        self.board3.move_piece(3, 2)
        self.board3.possible_captures()

        self.assertEqual(self.board3[3, 2].captured_pieces, [[(4, 3), (4, 5)]])

    def test_possible_moves4(self):
        self.board4 = Board()
        self.board4.change_color()
        self.board4.active_piece = (2, 1)
        self.board4.move_piece(4, 3)
        self.board4.active_piece = (2, 5)
        self.board4.move_piece(3, 4)
        self.board4.active_piece = (1, 4)
        self.board4.move_piece(2, 5)
        self.board4.change_color()

        self.assertEqual(self.board4[5, 4].moves_pos, [[(3, 2), (1, 4), (3, 6)]])

    def test_possible_captures4(self):
        self.board4 = Board()
        self.board4.change_color()
        self.board4.active_piece = (2, 1)
        self.board4.move_piece(4, 3)
        self.board4.active_piece = (2, 5)
        self.board4.move_piece(3, 4)
        self.board4.active_piece = (1, 4)
        self.board4.move_piece(2, 5)
        self.board4.change_color()

        self.assertEqual(self.board4[5, 4].captured_pieces, [[(4, 3), (2, 3), (2, 5)]])

    def test_move_piece(self):
        number = self.board[5, 2].number
        self.board.active_piece = (5, 2)
        self.board.current_color = "light"
        self.board.move_piece(4, 3)
        self.assertIsNone(self.board[5, 2])
        self.assertIsNotNone(self.board[4, 3])

        for piece in self.board.light_pieces:
            if piece.number == number:
                self.assertIs(piece, self.board[4, 3])

    def test_make_king(self):
        self.board.make_king(5, 6)
        self.assertIsInstance(self.board[5, 6], King)

    def test_capture(self):
        self.board.current_color = "dark"
        number = self.board[5, 6].number
        self.board.capture(5, 6)
        self.assertIsNone(self.board[5, 6])

        for piece in self.board.light_pieces:
            self.assertNotEqual(piece.number, number)

    def test_deactivate_current_piece(self):
        self.board[5, 4].active = True
        self.board.active_piece = (5, 4)
        self.board.deactivate_current_piece()
        self.assertFalse(self.board[5, 4].active)


class TestGameInterface(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        root = tk.Tk()
        root.resizable(False, False)
        self.gi = GameInterface(root)
        self.gi.start_game()

    def test_remove_symbols(self):
        self.gi.king_symbols.append("T1")
        self.gi.remove_symbols()
        self.assertEqual(self.gi.king_symbols, [])

    def test_remove_field_selections(self):
        self.gi.field_selections.append([(2, 3)])
        self.gi.remove_field_selection()
        self.assertEqual(self.gi.field_selections, [])

    def test_game_info_light(self):
        self.gi.board.current_color = "light"
        self.gi.game_info()
        self.assertEqual(self.gi.game_info_color["text"], "białych")
        self.assertEqual(self.gi.game_info_color["fg"], "#FFFFFF")

    def test_game_info_dark(self):
        self.gi.board.current_color = "dark"
        self.gi.game_info()
        self.assertEqual(self.gi.game_info_color["text"], "czarnych")
        self.assertEqual(self.gi.game_info_color["fg"], "#000000")

    def test_create_king(self):
        self.gi.create_king(5, 6)
        self.assertIsNot(self.gi.king_symbols, [])

    def test_game_state(self):
        self.gi.board.dark_left = 0
        self.gi.board.light_left = 2
        self.gi.game_state()
        self.assertEqual(self.gi.game_info_text["text"], "Wygrały")
        self.assertEqual(self.gi.game_info_color["text"], "białe!")

        self.gi.board.dark_left = 2
        self.gi.board.light_left = 0
        self.gi.game_state()
        self.assertEqual(self.gi.game_info_text["text"], "Wygrały")
        self.assertEqual(self.gi.game_info_color["text"], "czarne!")

        self.gi.board.light_left = 2
        self.gi.board.no_capture_light = 0
        self.gi.board.no_capture_dark = 0
        self.gi.game_state()
        self.assertEqual(self.gi.game_info_text["text"], "Remis!")
        self.assertEqual(self.gi.game_info_color["text"], "")


if __name__ == "__main__":
    unittest.main()