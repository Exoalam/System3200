from flask import Flask, render_template, url_for, request
from flask_dropzone import Dropzone
from model import RRDBNet
from downscale import Downscale
from use_model import Generator
import os

app = Flask(__name__)
dropzone = Dropzone(app)

@app.route('/store', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        print("Hello")
        Downscale.save()
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join('Temp', f.filename))  
    return render_template('Store.html')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    if request.method == 'POST':
        if request.form.get('Restore') == 'Restore':
            Generator.output()
    return render_template('retrieve.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')
if __name__ == "__main__":
    app.run(debug=True)