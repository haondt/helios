from flask import Flask, jsonify, render_template

from app import views
from app import data
from app.data import Data

def MockData(state: Data):
    g1 = state.add_group("my fav websites")
    state.add_mark(g1.id, "google", "https://google.com")
    state.add_mark(g1.id, "facebook", "https://www.facebook.com")
    state.add_mark(g1.id, "youtube", "https://youtube.com")

    g2 = state.add_group("server")
    state.add_mark(g2.id, "infisical", "infisical.gabbro-ce")
    state.add_mark(g2.id, "plex", "plex.tv/web")
    state.add_mark(g2.id, "qbittorrent", "http://deluge:8080")

    g3 = state.add_group("i dunno man")
    state.add_mark(g3.id, "a link", "infisical.gabbro-ce")
    state.add_mark(g3.id, "another link", "plex.tv/web")
    state.add_mark(g3.id, "q third link", "http://deluge:8080")

def Helios(config):
    if 'data_file' not in config:
        config['data_file'] = './data.json'

    helios = Flask(__name__, template_folder='views/templates', static_folder='views/static')

    d = Data(config)
    MockData(d)
    views.apply(helios, d)

    return helios
        
