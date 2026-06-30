# -*- coding: utf-8 -*-
from flask import Flask

import ell

@ell.simple(model="gpt-4o-mini")
def hello(name: str):
    """You are a helpful assistant"""
    return f"Write a welcome message for {name}."

app = Flask(__name__)


@app.route('/')
#     app.run(debug=True)
def home():
    return hello("world")

if __name__ == '__main__':

