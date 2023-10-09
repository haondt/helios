from flask import Flask, jsonify, render_template, request
#from app import app

def apply(helios, data):
    @helios.route('/hx/marks/view')
    def get_marks():
        return render_template('marks-view.html', marks=data.state.marks)

    @helios.route('/hx/marks/view/<id>')
    def get_mark(id):
        mark = data.state.marks[0]
        return render_template('mark-view.html', mark=mark)

