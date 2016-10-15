O = 'o'
X = 'x'
BLANK = ' '
SIDE_SIZE = 3


class GameError(Exception):
    pass


class BadBoard(GameError):
    pass


class GameOver(GameError):
    pass


class NotMyTurn(GameError):
    pass


def other_player(player):
    if player == O:
        return X
    elif player == X:
        return O
    else:
        raise ValueError('{} is not a player'.format(player))


def player_has_won(board, player):
    for row in range(SIDE_SIZE):
        if all(board[row, col] == player for col in range(SIDE_SIZE)):
            return True
    for col in range(SIDE_SIZE):
        if all(board[row, col] == player for row in range(SIDE_SIZE)):
            return True
    if all(board[i, i] == player for i in range(SIDE_SIZE)):
        return True
    if all(board[i, SIDE_SIZE-i-1] == player for i in range(SIDE_SIZE)):
        return True


def _get_index(row, col):
    assert 0 <= row < SIDE_SIZE
    assert 0 <= col < SIDE_SIZE
    return SIDE_SIZE*row + col


class Board:
    """
    Represents a board. Can only represent a valid board (board that arises in the game of tic tac toe).
    """
    def __init__(self, board_string):
        if len(board_string) != SIDE_SIZE**2:
            raise BadBoard('board string is the wrong size')
        if not all(letter in [O, X, BLANK] for letter in board_string):
            raise BadBoard('board string contains an illegal character')

        self.num_os = sum(letter == O for letter in board_string)
        self.num_xs = sum(letter == X for letter in board_string)
        if abs(self.num_os - self.num_xs) > 1:
            raise BadBoard('this board cannot arise in tic tac toe')

        self.string = board_string
        self.winner = self._get_winner()

    def __getitem__(self, pos):
        row, col = pos
        index = _get_index(row, col)
        return self.string[index]

    def new_board_with_move(self, player, row, col):
        index = _get_index(row, col)
        new_board_string = self.string[:index] + player + self.string[(index+1):]
        return Board(new_board_string)

    def is_full(self):
        return self.num_xs + self.num_os == SIDE_SIZE**2

    def _get_winner(self):
        o_wins = player_has_won(self, O)
        x_wins = player_has_won(self, X)
        if o_wins and x_wins:
            raise BadBoard('board where both players won is impossible')
        elif o_wins:
            return O
        elif x_wins:
            return X
        else:
            return None

    def possible_moves(self, player):
        return [self.new_board_with_move(player, row, col)
                for row in range(SIDE_SIZE) for col in range(SIDE_SIZE)
                if self[row, col] == BLANK]

    def __repr__(self):
        return self.string

    def __eq__(self, other):
        return isinstance(other, Board) and other.string == self.string


def best_move_with_outcome(board, player):
    """
    :param board: Board
    :param player: str (a player)
    :return: tuple with best move and winner (None if no winner)
    """
    # It would be better to memoize and safe computation.
    # Even better would be to build up a dictionary of boards and best responses (when the app starts, or outside the
    # app.

    if board.string == '         ':
        # a good move for beating humans and saves computation at game start
        return Board('    ' + player + '    '), None
    if board.winner:
        raise GameOver('{} already won!'.format(board.winner))
    if player == O and board.num_os > board.num_xs:
        raise NotMyTurn('not my turn')
    if player == X and board.num_xs > board.num_os:
        raise NotMyTurn('not my turn')

    moves = board.possible_moves(player)
    winning_moves = [move for move in moves if move.winner == player]
    if winning_moves:
        return winning_moves[0], player
    elif len(moves) == 1:  # only one choice, in which I don't win
        return moves[0], None
    else:
        moves_with_outcome = [(move, best_move_with_outcome(move, other_player(player))[1])
                              for move in moves]
        winning_moves = [move for move, outcome in moves_with_outcome if outcome == player]
        drawing_moves = [move for move, outcome in moves_with_outcome if outcome is None]
        if winning_moves:
            return winning_moves[0], player
        elif drawing_moves:
            return drawing_moves[0], None
        else:
            return moves[0], other_player(player)


