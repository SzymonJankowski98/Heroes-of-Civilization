from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
import cx_Oracle
import json

#cx_Oracle.init_oracle_client(lib_dir=r"D:\Program Files\OracleClient\instantclient_19_9")
cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\Szymon\Documents\instantclient_19_9")

app = Flask(__name__)
app.secret_key = "hoc1"
app.permanent_session_lifetime = timedelta(minutes=120)
db = cx_Oracle.connect("inf141229", "inf141229", "admlab2.cs.put.poznan.pl/dblab02_students.cs.put.poznan.pl")
cursor = db.cursor()

# with open('static/images/gold-ingots.png', 'rb') as f:
#     imgdata = f.read()
# cursor.callproc("AddResource", ['Gold', imgdata])
#
# with open('static/images/wood.png', 'rb') as f:
#     imgdata = f.read()
# cursor.callproc("AddResource", ['Wood', imgdata])
#
# with open('static/images/stone.png', 'rb') as f:
#     imgdata = f.read()
# cursor.callproc("AddResource", ['Stone', imgdata])
#
# with open('static/images/beam.png', 'rb') as f:
#     imgdata = f.read()
# cursor.callproc("AddResource", ['Iron', imgdata])
#
# with open('static/images/gem.png', 'rb') as f:
#     imgdata = f.read()
# cursor.callproc("AddResource", ['Crystal', imgdata])
# db.commit()


def get_games_info(name):
    ids = []
    cursor = db.cursor()
    cursor.execute(''' SELECT game_id FROM users_in_games WHERE user_name = :usr_name ''', usr_name=name)
    for i in cursor:
        ids.append(i)
    infos = []
    cursor.close()

    objType = db.gettype("G_INFO_TABLE")
    cursor = db.cursor()
    for g_id in ids:
        cursor.execute(''' SELECT * FROM table(:x)''', x=cursor.callfunc('game_info', objType, [g_id[0]]))
        for y in cursor:
            infos.append(list(y))
    cursor.close()

    nfull = []
    objType2 = db.gettype("NFULL_GAMES_TABLE")
    cursor = db.cursor()
    cursor.execute(''' SELECT * FROM table(:p) ''', p=cursor.callfunc("nfull_games_info", objType2, [name]))
    for rec in cursor:
        nfull.append(list(rec))
    cursor.close()

    return infos, nfull


def get_map(name, game_id):
    game_id = int(game_id)
    fields = []

    cursor = db.cursor()
    objType = db.gettype("GAME_MAP_TABLE")
    cursor.execute(''' SELECT * FROM table(:z) ''', z=cursor.callfunc("get_map", objType, [game_id]))
    for field in cursor:
        fields.append(list(field))
    print(fields)
    cursor.close()

    cursor = db.cursor()
    buildings = []
    objType = db.gettype("BUILDINGS_MAP_TABLE")
    cursor.execute(''' SELECT * FROM table(:ar) ''', ar=cursor.callfunc("get_buildings_map", objType, [game_id]))
    for building in cursor:
        buildings.append(list(building))
    print(buildings)
    cursor.close()

    cursor = db.cursor()
    units = []
    objType = db.gettype("UNITS_MAP_TABLE")
    cursor.execute(''' SELECT * FROM table(:ar) ''', ar=cursor.callfunc("get_units_map", objType, [game_id]))
    for unit in cursor:
        units.append(list(unit))
    print(units)
    cursor.close()

    cursor = db.cursor()
    units_info = []
    objType2 = db.gettype("UNITS_INFO_TABLE")
    cursor.execute(''' SELECT * FROM table(:x) ''', x=cursor.callfunc("get_units_info", objType2, []))
    for unit_info in cursor:
        units_info.append(list(unit_info))
    print(units_info)
    cursor.close()

    cursor = db.cursor()
    buildings_info = []
    objType = db.gettype("BUILDINGS_INFO_TABLE")
    cursor.execute(''' SELECT * FROM table(:ar) ''', ar=cursor.callfunc("get_buildings_info", objType, []))
    for building_info in cursor:
        buildings_info.append(list(building_info))
    print(buildings_info)
    cursor.close()

    cursor = db.cursor()
    resources_info = []
    objType = db.gettype("RESOURCES_INFO_TABLE")
    cursor.execute(''' SELECT * FROM table(:ar) ''', ar=cursor.callfunc("get_resources_info", objType, [game_id, name]))
    for resource_info in cursor:
        resources_info.append(list(resources_info))
    print(resources_info)
    cursor.close()

    return fields, buildings, units, units_info, buildings_info, resources_info


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


@app.route('/user', methods=["POST", "GET"])
def user_page():
    if "user" in session:
        user = session["user"]
        infos, nfull = get_games_info(user)
        if request.method == "POST":
            x_size = request.form['xs']
            y_size = request.form['ys']
            max_players = request.form['maxp']
            r_chances = request.form['chances']
            if len(x_size) > 0 or len(y_size) > 0 or len(max_players) > 0 or len(r_chances) > 0:
                cursor.callproc("CreateGame", [user, int(x_size), int(y_size), int(max_players), float(r_chances)])
                db.commit()
                return redirect(url_for("user_page"))
            else:
                return render_template("user_page.html", usr=user, games=infos, all_games=nfull)
        else:
            infos, nfull = get_games_info(user)
            return render_template("user_page.html", usr=user, games=infos, all_games=nfull)
    else:
        return redirect(url_for("login_page"))


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))


@app.route('/game/<game_id>')
def game(game_id):
    user = session["user"]
    fields, buildings, units, units_info, buildings_info, resources_info = get_map(user, int(game_id))
    return render_template('game.html', fields=fields, buildings=buildings, units=units, units_info=units_info, buildings_info=buildings_info, resources_info=resources_info)


if __name__ == '__main__':
    app.run()
