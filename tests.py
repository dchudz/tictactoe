import pytest
from tic import Board


def test_has_won():
    board = Board('xxxoo    ')
    assert board.winner == 'x'
