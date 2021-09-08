import random

from flask import Flask, render_template, request

application = app = Flask(__name__)


class GuessGame:
    def __init__( self ):
        self.comp_num = random.randint(1, 10)
        self.counter = 0
        self.game_over = False

    def increment_goes( self ):
        self.counter += 1

    def check_game_over( self, the_input ):
        # checks for whether the game is finished
        if the_input == self.comp_num or self.counter == 3:
            self.game_over = True
        if the_input == self.comp_num:
            return "You Won"
        if self.counter == 3:
            return "Maximum Guess limit: 3"
        return ""


global game
game = GuessGame()


@app.route("/", methods=['GET', 'POST'])
def index():
    global game
    message = ""

    if request.method == 'POST':
        game.increment_goes()
        form = request.form
        user_guess = int(form["guess"])
        if game.comp_num == user_guess:
            message = "Well done. You got it right!"
        elif game.comp_num > user_guess:
            message = "Too Low"
        else:
            message = "Too High"
        result = game.check_game_over(user_guess)
        if game.check_game_over(user_guess):
            return render_template("game-over.html", message=result)
    return render_template("index.html", message=message)


#if __name__ == '__main__':
    #app.run(debug=True)
