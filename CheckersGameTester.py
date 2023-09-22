import unittest
from CheckersGame import Checkers, Player


class TestCheckers(unittest.TestCase):
    """
    Contains unit tests for CheckersGame.py
    """
    def test_player_creation(self):
        """Tests that a player is created"""
        test_game = Checkers()
        first_player = test_game.create_player("Sam", "White")
        second_player = test_game.create_player("Nate", "Black")
        self.assertIs(test_game.check_name("Nate"), True)

    def test_movement(self):
        """Tests if player is created"""
        test_game = Checkers()
        first_player = test_game.create_player("Tony", "Black")
        second_player = test_game.create_player("Alyssa", "White")
        test_game.play_game("Tony", (6, 3), (5, 4))
        self.assertEqual(test_game.get_checker_details((5, 4)), "Black")

    def test_king(self):
        """Tests if piece becomes king"""
        test_game = Checkers()
        first_player = test_game.create_player("Tony", "Black")
        second_player = test_game.create_player("Alyssa", "White")
        test_game.play_game("Tony", (6, 3), (5, 4))
        test_game.play_game("Alyssa", (3, 6), (4, 5))
        test_game.play_game("Tony", (5, 4), (3, 6))
        test_game.play_game("Alyssa", (3, 4), (4, 5))
        test_game.play_game("Tony", (6, 1), (5, 2))
        test_game.play_game("Alyssa", (2, 5), (3, 4))
        test_game.play_game("Tony", (5, 2), (4, 3))
        test_game.play_game("Alyssa", (1, 4), (2, 5))
        test_game.play_game("Tony", (3, 6), (1, 4))
        self.assertEqual(test_game.get_checker_details((1, 4)), "Black_King")

    def test_captured_pieces(self):
        """Tests if captured pieces are accurate"""
        test_game = Checkers()
        first_player = test_game.create_player("Tony", "Black")
        second_player = test_game.create_player("Alyssa", "White")
        test_game.play_game("Tony", (6, 3), (5, 4))
        test_game.play_game("Alyssa", (3, 6), (4, 5))
        test_game.play_game("Tony", (5, 4), (3, 6))
        test_game.play_game("Alyssa", (3, 4), (4, 5))
        test_game.play_game("Tony", (6, 1), (5, 2))
        test_game.play_game("Alyssa", (2, 5), (3, 4))
        test_game.play_game("Tony", (5, 2), (4, 3))
        test_game.play_game("Alyssa", (1, 4), (2, 5))
        self.assertGreaterEqual(test_game.play_game("Tony", (3, 6), (1, 4)), 2)

    def test_print_board(self):
        """Tests if the board is printed in an array"""
        test_game = Checkers()
        self.assertIn(test_game.print_board(), ([None, 'White', None, 'White', None, 'White', None, 'White']))

    def test_winner(self):
        """Tests if board returns 'Game has not ended'"""
        test_game = Checkers()
        first_player = test_game.create_player("Tony", "Black")
        second_player = test_game.create_player("Alyssa", "White")
        test_game.play_game("Tony", (6, 3), (5, 4))
        test_game.play_game("Alyssa", (3, 6), (4, 5))
        test_game.play_game("Tony", (5, 4), (3, 6))
        test_game.play_game("Alyssa", (3, 4), (4, 5))
        self.assertNotEqual(test_game.game_winner(), "Alyssa")


if __name__ == '__main__':
    unittest.main()
