from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = "hoc1"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login_page():
    if request.method == 'POST':
        user = request.form["nm"]
        password = request.form["pw"]
        session["user"] = user
        return redirect(url_for("user_page"))
    else:
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


if __name__ == '__main__':
    app.run()
