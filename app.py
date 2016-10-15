from flask import Flask, request
from tic import Board, GameError, best_move_with_outcome, O

app = Flask(__name__)
ME = O

@app.errorhandler(GameError)
def bad_board(e):
    return str(e), 400


@app.route('/')
def index():
    try:
        board_string = request.args['board']
    except KeyError:
        return 'please provide a board in the "board" query parameter', 400

    board = Board(board_string)
    return best_move_with_outcome(board, ME)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)