# forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class MinesweeperForm(FlaskForm):
    game_type = SelectField("Game Type", choices=[("normal", "Normal"), ("ai", "AI")])
    game_mode = SelectField("Game Mode", choices=[("easy", "Easy"), ("normal", "Normal"), ("hard", "Hard"), ("custom", "Custom")])
    play_button = SubmitField("Play")
