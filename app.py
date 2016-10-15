from flask import Flask, request
from tic import Board, BadBoard

app = Flask(__name__)


@app.errorhandler(BadBoard)
def bad_board(e):
    return str(e), 400


@app.route('/')
def index():
    try:
        board_string = request.args['board']
    except KeyError:
        return 'please provide a board in the "board" query parameter', 400

    board = Board(board_string)
    return 'hi'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)