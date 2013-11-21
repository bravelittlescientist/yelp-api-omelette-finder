import os
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def run():
    return render_template("omelettes.html", res=[], location="")

@app.route('/omelettes', methods=["POST"])
def yelp_search():
    term = request.form['location']
    return render_template("omelettes.html", res=[1,2,3], location=term)
