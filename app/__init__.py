from flask import Flask, jsonify, render_template

from app import views
from app import data
from app.data import Data

def Helios(config):
    if 'data_file' not in config:
        config['data_file'] = './data.json'
    d = Data(config)
    d.load()

    helios = Flask(__name__, template_folder='views/templates', static_folder='views/static')
    views.apply(helios, d)

    return helios
