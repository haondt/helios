from flask import Flask, jsonify, render_template

from .marks import apply as marks_apply
from .groups import apply as groups_apply

def apply(helios, data):
    marks_apply(helios, data)
    groups_apply(helios, data)

    @helios.route('/', methods=['GET'])
    def home():
        return render_template("index.html", state=data.state)
