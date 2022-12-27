from flask import Flask, render_template, url_for, request, send_file
from flask_dropzone import Dropzone
from model import RRDBNet
from downscale import Downscale
from Generate import Generate
import os
import re
app = Flask(__name__)
dropzone = Dropzone(app)
select=[]
@app.route('/store', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
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
    filepath=[]
    for root, dirnames, filenames in os.walk("Temp"):
            for filename in filenames:
                if re.search("\.(jpg|jpeg|JPEG|png|bmp|tiff)$", filename):
                    filepath.append(os.path.join(root, filename))
    if request.method == "POST":
        if request.form.get('Restore') == 'Restore':
            select.append(request.form.get('images'))
            Generate.esrgan(request.form.get('images'))
                           
        if request.form.get('Download') == 'Download':
            path = select[0]
            select.clear
            return send_file(path, as_attachment=True)        
    return render_template('retrieve.html', toPass=filepath)
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')
if __name__ == "__main__":
    app.run(debug=True)