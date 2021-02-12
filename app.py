from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r"D:\Program Files\OracleClient\instantclient_19_9")
# cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\Szymon\Documents\instantclient_19_9")

app = Flask(__name__)
app.secret_key = "hoc1"
app.permanent_session_lifetime = timedelta(minutes=5)
db = cx_Oracle.connect("inf141229", "inf141229", "admlab2.cs.put.poznan.pl/dblab02_students.cs.put.poznan.pl")
cursor = db.cursor()


def get_games_info(name):
    print(name)
    ids = []
    cursor.execute(''' SELECT game_id FROM users_in_games WHERE user_name = :usr_name ''', usr_name=name)
    for i in cursor:
        ids.append(i)
    infos = []
    objType = db.gettype("G_INFO_TABLE")
    for g_id in ids:
        cursor.execute(''' SELECT * FROM table(:x)''', x=cursor.callfunc('game_info', objType, [name, g_id[0]]))
        for y in cursor:
            infos.append(list(y))

    return infos


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login_page():
    if request.method == 'POST':
        session.permanent = True
        user = request.form["nm"]
        password = request.form["pw"]
        if cursor.callfunc("goodPass", int, [user, password]) > 0:
            session["user"] = user
            return redirect(url_for("user_page"))
        else:
            flash("Niepoprawna nazwa użytkownika lub hasło.")
            return render_template('login_page.html')
    else:
        if "user" in session:
            return redirect(url_for("user_page"))
        return render_template('login_page.html')


@app.route('/register', methods=["POST", "GET"])
def register_page():
    if request.method == 'POST':
        usr = request.form["nm"]
        usr_pw = request.form["pw"]
        usr_rpw = request.form["rpw"]
        if usr_rpw != usr_pw:
            flash("Hasła nie są takie same.")
        else:
            if cursor.callfunc("isRegistered", int, [usr]) > 0:
                flash("Nazwa użytkownika jest już zajęta.")
            else:
                cursor.callproc("RegisterPlayer", [usr, usr_pw])
                db.commit()
                session.permanent = True
                session["user"] = usr
                return redirect(url_for("user_page"))
    return render_template('register_page.html')


@app.route('/user')
def user_page():
    if "user" in session:
        user = session["user"]
        infos = get_games_info(user)
        print(infos)
        return render_template("user_page.html", usr=user, ids_list=infos)
    else:
        return redirect(url_for("login_page"))


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))


@app.route('/game')
def game():
    return render_template('game.html')


if __name__ == '__main__':
    app.run()
