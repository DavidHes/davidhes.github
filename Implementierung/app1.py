from flask import Flask
import os
import db #importieren die bd und die ganzene funktionalität

app = Flask(__name__)

#mit return an den web browser was zurückgeben - hat keine Eingabeparametwr - immer aufgerufen wenn client die URL aufruft
#@ erwickelt die Funktion

@app.route('/')
def index():
        return "Hello, World!"

#listen von todos anzeigen auf der webseite

@app.route('/Lists/')
def Lists():
        return 'Todo: shoq all to-do Lists'

@app.route('/Lists/<')
def Lists():
        return 'Todo: shoq all to-do Lists'