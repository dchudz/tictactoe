import pytest
from tic import Board, best_move_with_outcome, GameOver, BadBoard, NotMyTurn
from flask_testing import TestCase

from app import app


def test_has_won():
    board = Board('xxxoo    ')
    assert board.winner == 'x'


def test_best_move_one_step():
    move, outcome = best_move_with_outcome(Board('xx oo    '), 'x')
    assert move == Board('xxxoo    ')
    assert outcome == 'x'

    move, outcome = best_move_with_outcome(Board('xx oo    '), 'o')
    assert move == Board('xx ooo   ')
    assert outcome == 'o'


def test_best_move_two_steps():
    board = Board(
    ' x ' + \
    ' o ' + \
    '   ')

    move, outcome = best_move_with_outcome(board, 'o')
    assert outcome == 'o'


def test_already_won():
    board = Board(
    'xxx' + \
    'oo ' + \
    '   ')
    with pytest.raises(GameOver):
        best_move_with_outcome(board, 'o')


def test_cant_be_my_turn():
    board = Board(
    'xxo' + \
    'oo ' + \
    '   ')
    with pytest.raises(NotMyTurn):
        best_move_with_outcome(board, 'o')


class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_something(self):
        response = self.client.get("/", query_string={'board': 'oo xx    '})
        assert response.status_code == 200
        assert response.data.decode() == 'oooxx    '