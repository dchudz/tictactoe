from flask import Flask, request

app = Flask(__name__)


class BadBoard(Exception):
    pass

@app.errorhandler(BadBoard)
def bad_board(e):
    return str(e), 400


class Board:
    def __init__(self, board_string):
        pass
    pass

@app.route('/')
def index():
    try:
        board_string = request.args['board']
    except KeyError:
        return 'please provide a board in the "board" query parameter', 400

    return 'hey there'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)