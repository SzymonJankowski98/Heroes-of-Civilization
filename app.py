from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hoc1"
app.permanent_session_lifetime = timedelta(days=1)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login_page():
    if request.method == 'POST':
        session.permanent = True
        user = request.form["nm"]
        # password = request.form["pw"]
        session["user"] = user
        return redirect(url_for("user_page"))
    else:
        if "user" in session:
            return redirect(url_for("user_page"))
        return render_template('login_page.html')


@app.route('/register', methods=["POST", "GET"])
def register_page():
    return render_template('register_page.html')


@app.route('/user')
def user_page():
    if "user" in session:
        user = session["user"]
        return render_template("user_page.html", usr=user)
    else:
        return redirect(url_for(login_page))


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))

@app.route('/game')
def game():
    return render_template('game.html')


if __name__ == '__main__':
    app.run()
