from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "arglebargle42"

boggle_game = Boggle()

@app.route("/")
def landing_page():
    """Display the Boggle board on the landing page"""

    gameboard = boggle_game.make_board()
    session['board'] = gameboard
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("index.html", board=gameboard,
                           highscore=highscore,
                           nplays=nplays)


@app.route("/check-word")
def check_word():
    """Check if the user-submitted word is in the game's dictionary."""

    word = request.args["word"]
    gameboard = session["board"]
    response = boggle_game.check_valid_word(gameboard, word)

    return jsonify({'result': response})


@app.route("/show-score", methods=["POST"])
def show_score():
    """Display the user's score. Also, update the number of plays, and possibly update the game high score."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)