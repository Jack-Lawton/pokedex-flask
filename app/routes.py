from app import app
from flask import render_template, url_for
import requests
import json
import ast
import os

if not os.path.exists("api-cache.txt"):
    import cache_data

f = open("api-cache.txt", "r")
pokedex_dict_raw = ast.literal_eval(f.read())

pokedex_dict = {}

for i in range(1000):
    if i in pokedex_dict_raw:
        pokedex_dict[i] = pokedex_dict_raw[i]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', pokedex = pokedex_dict, entries = len(pokedex_dict)+1)

@app.route('/type/<f>')
def type_filter(f):
    type_dict = {}
    for key, value in pokedex_dict.items():
        if f in value["type"]:
            type_dict[len(type_dict) + 1] = value
    return render_template('index.html', pokedex = type_dict, entries = len(type_dict)+1)

