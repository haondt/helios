from flask import Flask, jsonify, render_template

from app import views
from app import data
from app.data import Data

def MockData(state: Data):
    g1 = state.add_group("frequent sites")
    state.add_mark(g1.id, "google", "https://google.com")
    state.add_mark(g1.id, "facebook", "https://www.facebook.com")
    state.add_mark(g1.id, "reddit", "old.reddit.com")

    g2 = state.add_group("home server")
    state.add_mark(g2.id, "infisical", "infisical.gabbro-ce").icon = "fa-solid fa-infinity"
    state.add_mark(g2.id, "plex", "plex.tv/web").icon = "fa-solid fa-play"
    state.add_mark(g2.id, "qbittorrent", "http://deluge:8080").icon = "fa-solid fa-download"

    g3 = state.add_group("videos")
    state.add_mark(g3.id, "youtube", "https://youtube.com").icon = "fa-brands fa-youtube"
    state.add_mark(g3.id, "netflix", "netflix.com").icon = "fa-solid fa-n"
    state.add_mark(g3.id, "twitch", "twitch.tv").icon = "fa-brands fa-twitch"

def Helios(config):
    if 'data_file' not in config:
        config['data_file'] = './data.json'

    helios = Flask(__name__, template_folder='views/templates', static_folder='views/static')

    d = Data(config)
    MockData(d)
    views.apply(helios, d)

    return helios
        
