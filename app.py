from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/store')
def store():
    return render_template('Store.html')
@app.route('/retrieve')
def retrieve():
    return render_template('retrieve.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
if __name__ == "__main__":
    app.run(debug=True)