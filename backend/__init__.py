import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

secret_key = os.getenv("SECRET_KEY")

# Create Flask app
app = Flask(__name__)
app.secret_key = secret_key

# import blueprints
from backend.minesweeper.routes import minesweeper
from backend.main.routes import main
from backend.tictactoe.routes import tictactoe

# register blueprints
app.register_blueprint(minesweeper)
app.register_blueprint(main)
app.register_blueprint(tictactoe)

