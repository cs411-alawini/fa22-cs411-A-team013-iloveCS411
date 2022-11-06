""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route("/")
def homepage():
    """ returns rendered homepage """

    return render_template("login.html")