from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET KEY"] = "itsasecret"
app.secret_key = "okaythen"

boggle_game = Boggle()

@app.route('/')
def homepage():
    """ Create board
        Set board to session
        Get session high score
        Get session number of tries
        Return populated board
    """
    board = boggle_game.make_board()
    session['board'] = board
    high_score = session.get("high_score", 0)
    num_games = session.get("num_games", 0)

    return render_template('index.html', board=board, high_score=high_score, num_games=num_games)

@app.route('/check_word')
def check_word():
    """ Get word from request.args
        Check word against dict_file
    """
    word = request.args["word"]
    board = session["board"]
    res = boggle_game.check_valid_word(board, word)

    return jsonify({ "result": res })

@app.route('/post_score', methods=["POST"])
def post_score():
    """ check score and number of tries
        against session scores
        reset high_score if new score is highest
    """
    score = request.json["score"]
    high_score = session.get("high_score", 0)
    num_games = session.get("num_games", 0)

    session["num_games"] = num_games + 1
    session["high_score"] = max(score, high_score)

    return jsonify(newHighScore = score > high_score)

