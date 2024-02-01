from flask import render_template, request, Blueprint
from backend.minesweeper.forms import MinesweeperForm
from backend.minesweeper.utils import generate_board, print_board

# Create blueprint
minesweeper = Blueprint("minesweeper", __name__, url_prefix="/minesweeper")

@minesweeper.route("/play", methods=["GET", "POST"])
def play():
    form = MinesweeperForm()
    board = None

    if request.method == "POST" and form.validate_on_submit():
        # Handle form submission if needed
        game_type = form.game_type.data
        game_mode = form.game_mode.data
        print(game_type, game_mode)

        board_size = (5, 5)
        mines = 10

        # Generate Minesweeper board
        board = generate_board(board_size, mines)
        print_board(board)

    return render_template("minesweeper.html", form=form, board=board)
