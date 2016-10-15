import pytest
from tic import Board, best_move_with_outcome


def test_has_won():
    board = Board('xxxoo    ')
    assert board.winner == 'x'

def test_best_move():
    move, outcome = best_move_with_outcome(Board('xx oo    '), 'x')
    assert move == Board('xxxoo    ')
    assert outcome == 'x'

    move, outcome = best_move_with_outcome(Board('xx oo    '), 'o')
    assert move == Board('xx ooo   ')
    assert outcome == 'o'