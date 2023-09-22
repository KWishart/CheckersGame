class OutofTurn(Exception):
    """
    Raised when player moves out of turn
    """
    pass


class InvalidSquare(Exception):
    """
    Raised when player attempts to move a piece that isn’t theirs or square_location doesn't exist
    """
    pass


class InvalidPlayer(Exception):
    """
    Raised if player_name isn’t valid
    """
    pass


class Checkers:
    """
    Represents a game of Checkers
    """
    def __init__(self):
        self._board = [['x', 'w', 'x', 'w', 'x', 'w', 'x', 'w'],    # 'x' = invalid movement
                       ['w', 'x', 'w', 'x', 'w', 'x', 'w', 'x'],    # ' ' = empty square
                       ['x', 'w', 'x', 'w', 'x', 'w', 'x', 'w'],    # 'w' = white piece
                       [' ', 'x', ' ', 'x', ' ', 'x', ' ', 'x'],    # 'b' = black piece
                       ['x', ' ', 'x', ' ', 'x', ' ', 'x', ' '],    # 'wk' = white king
                       ['b', 'x', 'b', 'x', 'b', 'x', 'b', 'x'],    # 'bk' = black king
                       ['x', 'b', 'x', 'b', 'x', 'b', 'x', 'b'],    # '3w' = triple white king
                       ['b', 'x', 'b', 'x', 'b', 'x', 'b', 'x']]    # '3b' = triple black king
        self._player1 = None
        self._player2 = None

    def create_player(self, player_name, piece_color):
        """Creates a player"""
        if self._player1 is None:
            self._player1 = Player(player_name, piece_color)
            if self._player1.get_piece_color() == 'Black':
                self._player1.change_turn(True)
        elif self._player2 is None:
            self._player2 = Player(player_name, piece_color)
            if self._player2.get_piece_color() == 'Black':
                self._player2.change_turn(True)
        else:
            return "There are already 2 players"

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """Moves player's piece if valid"""
        if self.check_name(player_name) is True:
            if self._player1.get_turn() is True:  # Player 1's turn
                self.make_move(self._player1, starting_square_location, destination_square_location)
                self._player1.change_turn(False)
                self._player2.change_turn(True)
                return self._player1.get_captured_pieces_count()

            if self._player2.get_turn() is True:  # Player 2's turn
                self.make_move(self._player2, starting_square_location, destination_square_location)
                self._player2.change_turn(False)
                self._player1.change_turn(True)
                return self._player2.get_captured_pieces_count()

            else:
                raise OutofTurn

    def check_name(self, player_name):
        """Checks if the player name is valid"""
        if player_name == self._player1.get_name():
            return True
        if player_name == self._player2.get_name():
            return True
        else:
            raise InvalidPlayer

    def make_move(self, player, starting_square_location, destination_square_location):
        """Moves player's piece if possible"""
        start_row, start_column = starting_square_location
        start_row -= 1
        start_column -= 1
        end_row, end_column = destination_square_location
        end_row -= 1
        end_column -= 1

        if self._board[start_row][start_column] == 'w':     # white is moving
            if player.get_piece_color() == 'White':
                self._board[start_row][start_column] = ' '  # exchange places
                self._board[end_row][end_column] = 'w'
                if end_column > start_column:   # if the move was to the right
                    if self._board[start_row + 1][start_column + 1] == 'b':
                        self._board[start_row + 1][start_column + 1] = ' '
                        player.add_captured_piece()
                        self.check_bottom_end_board(player, end_row, end_column)  # check if piece reached end of board
                        return
                    return
                if end_column < start_column:   # if the move was to the left
                    if self._board[start_row + 1][start_column - 1] == 'b':
                        self._board[start_row + 1][start_column - 1] = ' '
                        player.add_captured_piece()
                        self.check_bottom_end_board(player, end_row, end_column)  # check if piece reached end of board
                        return
                    return
            else:
                raise InvalidSquare

        if self._board[start_row][start_column] == 'b':     # black is moving
            if player.get_piece_color() == 'Black':
                self._board[start_row][start_column] = ' '  # exchange places
                self._board[end_row][end_column] = 'b'
                if end_column > start_column:   # if the move was to the right
                    if self._board[start_row - 1][start_column + 1] == 'w':
                        self._board[start_row - 1][start_column + 1] = ' '
                        player.add_captured_piece()
                        self.check_top_end_board(player, end_row, end_column)  # check if piece reached end of board
                        return
                    return
                if end_column < start_column:   # if the move was to the left
                    if self._board[start_row - 1][start_column - 1] == 'w':
                        self._board[start_row - 1][start_column - 1] = ' '
                        player.add_captured_piece()
                        self.check_top_end_board(player, end_row, end_column)  # check if piece reached end of board
                        return
                    return
            else:
                raise InvalidSquare

            if self._board[start_row][start_column] == 'wk':  # white king is moving
                if player.get_piece_color() == 'White':
                    self._board[start_row][start_column] = ' '  # exchange places
                    self._board[end_row][end_column] = 'wk'
                    if end_column > start_column:  # if the move was to the right
                        if self._board[end_row - 1][end_column - 1] == 'b' or 'bk' or '3b':
                            self._board[end_row - 1][end_column - 1] = ' '
                            player.add_captured_piece()
                            self.check_top_end_board(player, end_row, end_column)  # check if piece reached end of board
                            return
                        return
                    if end_column < start_column:  # if the move was to the left
                        if self._board[end_row - 1][end_column + 1] == 'b' or 'bk' or '3b':
                            self._board[end_row - 1][end_column + 1] = ' '
                            player.add_captured_piece()
                            self.check_top_end_board(player, end_row, end_column)  # check if piece reached end of board
                            return
                        return
                else:
                    raise InvalidSquare

            if self._board[start_row][start_column] == 'bk':  # black king is moving
                if player.get_piece_color() == 'Black':
                    self._board[start_row][start_column] = ' '  # exchange places
                    self._board[end_row][end_column] = 'bk'
                    if end_column > start_column:  # if the move was to the right
                        if self._board[end_row + 1][end_column - 1] == 'w' or 'wk' or '3w':
                            self._board[end_row + 1][end_column - 1] = ' '
                            player.add_captured_piece()
                            self.check_bottom_end_board(player, end_row, end_column)  # check if piece reached end of
                            return                                                    # board
                        return
                    if end_column < start_column:  # if the move was to the left
                        if self._board[end_row + 1][end_column + 1] == 'w' or 'wk' or '3w':
                            self._board[end_row + 1][end_column + 1] = ' '
                            player.add_captured_piece()
                            self.check_bottom_end_board(player, end_row, end_column)  # check if piece reached end of
                            return                                                    # board
                        return
                else:
                    raise InvalidSquare

            if self._board[start_row][start_column] == '3w':  # triple white king is moving
                if player.get_piece_color() == 'White':
                    self._board[start_row][start_column] = ' '  # exchange places
                    self._board[end_row][end_column] = '3w'
                    if end_column > start_column:  # if the move was to the right
                        if self._board[end_row - 1][end_column - 1] == 'b' or 'bk' or '3b':
                            self._board[end_row - 1][end_column - 1] = ' '
                            player.add_captured_piece()
                            return
                        if self._board[end_row - 2][end_column - 2] == 'b' or 'bk' or '3b':  # if 2 pieces were captured
                            self._board[end_row - 2][end_column - 2] = ' '
                            player.add_captured_piece()
                            return
                        return
                    if end_column < start_column:  # if the move was to the left
                        if self._board[end_row - 1][end_column + 1] == 'b' or 'bk' or '3b':
                            self._board[end_row - 1][end_column + 1] = ' '
                            player.add_captured_piece()
                            return
                        if self._board[end_row - 2][end_column + 2] == 'b' or 'bk' or '3b':  # if 2 pieces were captured
                            self._board[end_row - 2][end_column + 2] = ' '
                            player.add_captured_piece()
                            return
                        return
                else:
                    raise InvalidSquare

            if self._board[start_row][start_column] == '3b':  # triple black king is moving
                if player.get_piece_color() == 'Black':
                    self._board[start_row][start_column] = ' '  # exchange places
                    self._board[end_row][end_column] = '3b'
                    if end_column > start_column:  # if the move was to the right
                        if self._board[end_row + 1][end_column - 1] == 'w' or 'wk' or '3w':
                            self._board[end_row + 1][end_column - 1] = ' '
                            player.add_captured_piece()
                            return
                        if self._board[end_row + 2][end_column - 2] == 'w' or 'wk' or '3w':  # if 2 pieces were captured
                            self._board[end_row + 2][end_column - 2] = ' '
                            player.add_captured_piece()
                            return
                        return
                    if end_column < start_column:  # if the move was to the left
                        if self._board[end_row + 1][end_column + 1] == 'w' or 'wk' or '3w':
                            self._board[end_row + 1][end_column + 1] = ' '
                            player.add_captured_piece()
                            return
                        if self._board[end_row + 2][end_column + 2] == 'w' or 'wk' or '3w':  # if 2 pieces were captured
                            self._board[end_row + 2][end_column + 2] = ' '
                            player.add_captured_piece()
                            return
                        return
                else:
                    raise InvalidSquare

            else:
                raise InvalidSquare

        else:
            raise InvalidSquare

    def check_top_end_board(self, player, end_row, end_column):
        """Checks if a piece reached the top end of the board"""
        if end_row - 1 == -1:
            if self._board[end_row][end_column] == 'b':
                self._board[end_row][end_column] = 'bk'
                player.add_king_count()
            if self._board[end_row][end_column] == 'wk':
                self._board[end_row][end_column] = '3w'
                player.add_triple_king_count()
        else:
            return

    def check_bottom_end_board(self, player, end_row, end_column):
        """Checks if a piece reached the bottom end of the board"""
        if end_row + 1 == 9:
            if self._board[end_row][end_column] == 'w':
                self._board[end_row][end_column] = 'wk'
                player.add_king_count()
            if self._board[end_row][end_column] == 'bk':
                self._board[end_row][end_column] = '3b'
                player.add_triple_king_count()
        else:
            return

    def get_checker_details(self, square_location):
        """Returns information about a square location"""
        row, column = square_location
        row -= 1
        column -= 1
        if self._board[row][column] == ' ':
            return None
        if self._board[row][column] == 'x':
            return None
        if self._board[row][column] == 'w':
            return 'White'
        if self._board[row][column] == 'b':
            return 'Black'
        if self._board[row][column] == 'wk':
            return 'White_King'
        if self._board[row][column] == 'bk':
            return 'Black_King'
        if self._board[row][column] == '3w':
            return 'Triple_White_King'
        if self._board[row][column] == '3b':
            return 'Triple_Black_King'
        else:
            raise InvalidSquare

    def print_board(self):
        """Returns the board as an array"""
        board = []
        for row in self._board:
            board_row = []
            for column in row:
                if column == ' ':
                    board_row.append(None)
                if column == 'x':
                    board_row.append(None)
                if column == 'w':
                    board_row.append('White')
                if column == 'b':
                    board_row.append('Black')
                if column == 'wk':
                    board_row.append('White King')
                if column == 'bk':
                    board_row.append('Black King')
                if column == '3w':
                    board_row.append('Triple White King')
                if column == '3b':
                    board_row.append('Triple Black King')
            board.append(board_row)
        print(board)

    def game_winner(self):
        """Returns the name of player that won or if game isn't over returns 'Game has not ended'"""
        if self._player1.get_captured_pieces_count() == 12:
            return self._player1.get_name()
        if self._player2.get_captured_pieces_count() == 12:
            return self._player2.get_name()
        else:
            return 'Game has not ended'


class Player:
    """
    Represents a player
    """
    def __init__(self, player_name, piece_color):
        self._player_name = player_name
        self._piece_color = piece_color
        self._player_turn = False
        self._captured_pieces_count = 0
        self._king_count = 0
        self._triple_king_count = 0

    def get_name(self):
        """Returns the player name"""
        return self._player_name

    def get_turn(self):
        """Returns if it is the player's turn"""
        return self._player_turn

    def change_turn(self, turn_value):
        """Changes if it is the player's turn or not"""
        self._player_turn = turn_value

    def get_piece_color(self):
        """Returns the player's piece color"""
        return self._piece_color

    def add_king_count(self):
        """Adds one to the amount of king pieces the player has"""
        self._king_count += 1

    def get_king_count(self):
        """Returns the number of king pieces the player has"""
        return self._king_count

    def add_triple_king_count(self):
        """Adds one to the amount of triple king pieces the player has"""
        self._triple_king_count += 1

    def get_triple_king_count(self):
        """Returns the number of triple king pieces the player has"""
        return self._triple_king_count

    def add_captured_piece(self):
        """Adds one to amount of captured pieces the player has"""
        self._captured_pieces_count += 1

    def get_captured_pieces_count(self):
        """Returns the number of opponent pieces the player has captured"""
        return self._captured_pieces_count


def main():
    game = Checkers()
    Player1 = game.create_player("Adam", "White")
    Player2 = game.create_player("Lucy", "Black")
    game.play_game("Lucy", (5, 6), (4, 7))
    game.play_game("Adam", (2,1), (3,0))
    game.get_checker_details((3,1))

    try:
        game.play_game(Player2, (3, 4), (6, 2))
    except InvalidSquare:
        print("This square location does not exist or you do not own the piece present.")


if __name__ == '__main__':
    main()
