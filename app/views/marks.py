from flask import Flask, jsonify, render_template, request
#from app import app

def apply(helios, data):
    @helios.route('/hx/mark/<id>')
    def get_mark(id):
        mark = data.state.marks[0]
        return render_template('mark.html', mark=mark)

