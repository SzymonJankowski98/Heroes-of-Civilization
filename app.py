from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login_page.html')


@app.route('/register')
def register_page():
    return render_template('register_page.html')


if __name__ == '__main__':
    app.run()
