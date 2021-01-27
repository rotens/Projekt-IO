import unittest

from board import Board


class TestBoard(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = Board()

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

    def test_block_other_pieces(self):
        pass


if __name__ == "__main__":
    unittest.main()