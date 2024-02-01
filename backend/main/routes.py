from flask import Blueprint, render_template, request, redirect, url_for, jsonify

# Create blueprint
main = Blueprint("main", __name__, url_prefix="/")

@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html")
