tictactoe = Blueprint("tictactoe", __name__, url_prefix="/tictactoe")

@tictactoe.route("/play", methods=["GET", "POST"])
def play():
            board = None
            board_size 
         # Generate Minesweeper board
            board = [[''*3]*3]
            print_board(board)

                                                                                                return render_template("tictactoe.html", board=board)
