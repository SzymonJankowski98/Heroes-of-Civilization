from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
import cx_Oracle
from base64 import b64encode

#cx_Oracle.init_oracle_client(lib_dir=r"D:\Program Files\OracleClient\instantclient_19_9")
cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\Szymon\Documents\instantclient_19_9")

app = Flask(__name__)
app.secret_key = "hoc1"
app.permanent_session_lifetime = timedelta(minutes=120)
db = cx_Oracle.connect("inf141229", "inf141229", "admlab2.cs.put.poznan.pl/dblab02_students.cs.put.poznan.pl")

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
    objType1 = db.gettype("GAME_MAP_TABLE")
    cursor.execute(''' SELECT * FROM table(:z) ''', z=cursor.callfunc("get_map", objType1, [game_id]))
    for field in cursor:
        fields.append(list(field))
    #print(fields)
    cursor.close()

    cursor = db.cursor()
    buildings = []
    objType2 = db.gettype("BUILDINGS_MAP_TABLE")
    a = cursor.callfunc("get_buildings_map", objType2, [game_id])
    cursor.close()
    cursor = db.cursor()
    cursor.execute(''' SELECT * FROM table(:a) ''', a=a)
    for building in cursor:
        buildings.append(list(building))
    #print(buildings)
    cursor.close()

    cursor = db.cursor()
    units = []
    objType3 = db.gettype("UNITS_MAP_TABLE")
    cursor.execute(''' SELECT * FROM table(:b) ''', b=cursor.callfunc("get_units_map", objType3, [game_id]))
    for unit in cursor:
        units.append(list(unit))
    print(units)
    cursor.close()

    cursor = db.cursor()
    units_info = []
    objType4 = db.gettype("UNITS_INFO_TABLE")
    cursor.execute(''' SELECT * FROM table(:x) ''', x=cursor.callfunc("get_units_info", objType4, []))
    for unit_info in cursor:
        units_info.append(list(unit_info))
    #print(units_info)
    cursor.close()

    cursor = db.cursor()
    buildings_info = []
    objType5 = db.gettype("BUILDINGS_INFO_TABLE")
    cursor.execute(''' SELECT * FROM table(:c) ''', c=cursor.callfunc("get_buildings_info", objType5, []))
    for building_info in cursor:
        buildings_info.append(list(building_info))
    #print(buildings_info)
    cursor.close()

    cursor = db.cursor()
    resources_info = []
    objType6 = db.gettype("RESOURCES_INFO_TABLE")
    cursor.execute(''' SELECT * FROM table(:d) ''', d=cursor.callfunc("get_resources_info", objType6, [game_id, name]))
    for resource_info in cursor:
        resources_info.append(list(resource_info))
    #print(resources_info)
    cursor.close()

    return fields, buildings, units, units_info, buildings_info, resources_info


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login_page():
    if request.method == 'POST':
        cursor = db.cursor()
        session.permanent = True
        user = request.form["nm"]
        password = request.form["pw"]
        if cursor.callfunc("goodPass", int, [user, password]) > 0:
            session["user"] = user
            cursor.close()
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
        cursor = db.cursor()
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
                cursor.close()
                return redirect(url_for("user_page"))
    cursor.close()
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
                cursor = db.cursor()
                cursor.callproc("CreateGame", [user, int(x_size), int(y_size), int(max_players), float(r_chances)])
                db.commit()
                cursor.close()
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
    session["game_id"] = game_id
    user = session["user"]
    fields, buildings, units, units_info, buildings_info, resources_info = get_map(user, int(game_id))

    width = 0
    for i in fields:
        if i[1] > width:
            width = i[1]

    height = 0
    for i in fields:
        if i[0] > height:
            height = i[0]

    new_units = [[[] for i in range(width)] for j in range(height)]
    for i in units:
        new_units[i[0]-1][i[1]-1].append([i[2], i[3], i[4], i[5]])

    new_buildings = [[[] for i in range(width)] for j in range(height)]
    for i in buildings:
        new_buildings[i[0]-1][i[1]-1].append(i[2])

    new_units_info = dict()
    for i in units_info:
        new_units_info[i[0]] = [i[1], i[2], i[3], i[4], b64encode(i[5].read()).decode("utf-8")]

    new_buildings_info = dict()
    for i in buildings_info:
        new_buildings_info[i[0]] = b64encode(i[1].read()).decode("utf-8")

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]

    cursor6 = db.cursor()
    o = cursor6.callfunc("get_turn", int, [game_id])
    cursor6.close()

    return render_template('game.html', user_name=user, width=width, height=height, fields=fields, buildings=new_buildings, units=new_units, units_info=new_units_info, buildings_info=new_buildings_info, resources_info=new_resourcer_info, turn_number=o)


@app.route('/getturn', methods=["POST"])
def get_turn():
    game_id = session["game_id"]
    cursor16 = db.cursor()
    p = cursor16.callfunc("get_turn", int, [game_id])
    cursor16.close()

    return str(p)

@app.route('/nextturn', methods=["POST"])
def next_turn():
    game_id = session["game_id"]
    user = session["user"]
    cursor6 = db.cursor()
    cursor6.callproc("nextTurn", [game_id, user])
    cursor6.close()

    return "True"


@app.route('/science', methods=["POST"])
def science():
    user = session["user"]
    game_id = session["game_id"]

    science = []
    objType = db.gettype("SCIENCE_INFO_TABLE")
    cursor2 = db.cursor()
    h = cursor2.callfunc("get_available_science", objType, [game_id, user])
    cursor2.close()
    cursor = db.cursor()
    cursor.execute(''' SELECT * FROM table(:h) ''', h=h)
    for s in cursor:
        cursor3 = db.cursor()
        cursor3.execute(''' SELECT * FROM table(:l) ''', l=s[5])
        res = []
        for r in cursor3:
            res.append(r)
        science.append([s[0], s[1], b64encode(s[2].read()).decode("utf-8"), s[3], s[4], res])
        cursor3.close()

    cursor = db.cursor()
    resources_info = []
    objType = db.gettype("RESOURCES_INFO_TABLE")
    cursor.execute(''' SELECT * FROM table(:ar) ''', ar=cursor.callfunc("get_resources_info", objType, [game_id, user]))
    for resource_info in cursor:
        resources_info.append(list(resource_info))

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]
    cursor.close()

    return render_template('science.html', science=science, resources_info=new_resourcer_info)


@app.route('/doscience', methods=["POST"])
def do_science():
    user = session["user"]
    game_id = session["game_id"]
    science_name = request.values['name']

    cursor = db.cursor()
    cursor.callproc("doScience", [int(game_id), user, science_name])
    db.commit()

    cursor2 = db.cursor()
    resources_info = []
    objType = db.gettype("RESOURCES_INFO_TABLE")
    cursor2.execute(''' SELECT * FROM table(:a) ''', a=cursor.callfunc("get_resources_info", objType, [game_id, user]))
    for resource_info in cursor2:
        resources_info.append(list(resource_info))
    cursor2.close()

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]
    cursor.close()

    return render_template('resorces.html', resources_info=new_resourcer_info)


@app.route('/availablebuildings', methods=["POST"])
def available_buildings():
    user = session["user"]
    game_id = session["game_id"]
    x = request.values['x']
    y = request.values['y']

    available_buildings = []
    objType = db.gettype("AVAILABLE_BUILDINGS_TABLE")
    cursor2 = db.cursor()
    g = cursor2.callfunc("get_available_buildings", objType, [game_id, user, x, y])
    cursor2.close()
    cursor = db.cursor()
    cursor.execute(''' SELECT * FROM table(:g) ''', g=g)
    for building in cursor:
        cursor3 = db.cursor()
        cursor3.execute(''' SELECT * FROM table(:l) ''', l=building[5])
        costs = []
        for r in cursor3:
            costs.append(r)
        cursor3.close()

        cursor4 = db.cursor()
        cursor4.execute(''' SELECT * FROM table(:i) ''', i=building[6])
        income = []
        for r in cursor4:
            income.append(r)
        cursor4.close()

        available_buildings.append([building[0], building[1], b64encode(building[2].read()).decode("utf-8"), building[3], building[4], costs, income])
    cursor.close()

    cursor5 = db.cursor()
    resources_info = []
    objType = db.gettype("RESOURCES_INFO_TABLE")
    cursor5.execute(''' SELECT * FROM table(:r) ''', r=cursor5.callfunc("get_resources_info", objType, [game_id, user]))
    for resource_info in cursor5:
        resources_info.append(list(resource_info))

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]
    cursor5.close()

    return render_template('available_buildings.html', available_buildings=available_buildings, resources_info=new_resourcer_info, x=x, y=y)


@app.route('/yourbuildings', methods=["POST"])
def your_buildings():
    user = session["user"]
    game_id = session["game_id"]
    x = request.values['x']
    y = request.values['y']

    your_buildings = []
    objType10 = db.gettype("YOUR_BUILDINGS_TABLE")
    cursor2 = db.cursor()
    v = cursor2.callfunc("get_your_buildings", objType10, [game_id, user, x, y])
    cursor2.close()
    cursor = db.cursor()
    cursor.execute(''' SELECT * FROM table(:v) ''', v=v)
    for building in cursor:
        cursor3 = db.cursor()
        cursor3.execute(''' SELECT * FROM table(:l) ''', l=building[3])
        income = []
        for r in cursor3:
            income.append(r)
        cursor3.close()

        your_buildings.append([building[0], b64encode(building[1].read()).decode("utf-8"), building[2], income])
    cursor.close()

    cursor5 = db.cursor()
    resources_info = []
    objType = db.gettype("RESOURCES_INFO_TABLE")
    cursor5.execute(''' SELECT * FROM table(:r) ''', r=cursor5.callfunc("get_resources_info", objType, [game_id, user]))
    for resource_info in cursor5:
        resources_info.append(list(resource_info))

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]
    cursor5.close()

    print(your_buildings)

    return render_template('your_buildings.html', your_buildings=your_buildings, resources_info=new_resourcer_info, x=x, y=y)


@app.route('/buildbuilding', methods=["POST"])
def build_building():
    user = session["user"]
    game_id = session["game_id"]
    building_name = request.values['name']
    x = request.values['x']
    y = request.values['y']

    cursor = db.cursor()
    cursor.callproc("BuildBuilding", [int(game_id), x, y, building_name, user])
    db.commit()

    cursor2 = db.cursor()
    resources_info = []
    objType = db.gettype("RESOURCES_INFO_TABLE")
    cursor2.execute(''' SELECT * FROM table(:a) ''', a=cursor.callfunc("get_resources_info", objType, [game_id, user]))
    for resource_info in cursor2:
        resources_info.append(list(resource_info))
    cursor2.close()

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]
    cursor.close()

    return render_template('resorces.html', resources_info=new_resourcer_info)


@app.route('/availableunits', methods=["POST"])
def available_units():
    user = session["user"]
    game_id = session["game_id"]
    x = request.values['x']
    y = request.values['y']

    available_units = []
    objType = db.gettype("AVAILABLE_UNIT_TABLE")
    cursor2 = db.cursor()
    f = cursor2.callfunc("get_available_units", objType, [game_id, user, x, y])
    cursor2.close()
    cursor = db.cursor()
    cursor.execute(''' SELECT * FROM table(:f) ''', f=f)
    for unit in cursor:
        cursor3 = db.cursor()
        cursor3.execute(''' SELECT * FROM table(:l) ''', l=unit[9])
        costs = []
        for r in cursor3:
            costs.append(r)
        cursor3.close()

        available_units.append([unit[0], unit[1], unit[2], unit[3], unit[4], unit[5], b64encode(unit[6].read()).decode("utf-8"), unit[7], unit[8], costs])
    cursor.close()

    cursor5 = db.cursor()
    resources_info = []
    objType = db.gettype("RESOURCES_INFO_TABLE")
    cursor5.execute(''' SELECT * FROM table(:r) ''', r=cursor5.callfunc("get_resources_info", objType, [game_id, user]))
    for resource_info in cursor5:
        resources_info.append(list(resource_info))

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]
    cursor5.close()

    print(available_units)

    return render_template('available_units.html', available_units=available_units, resources_info=new_resourcer_info, x=x, y=y)


@app.route('/yourunits', methods=["POST"])
def your_units():
    user = session["user"]
    game_id = session["game_id"]
    x = request.values['x']
    y = request.values['y']

    your_units = []
    objType9 = db.gettype("YOUR_UNITS_TABLE")
    cursor2 = db.cursor()
    e = cursor2.callfunc("get_your_units", objType9, [game_id, user, x, y])
    cursor2.close()
    cursor = db.cursor()
    cursor.execute(''' SELECT * FROM table(:e) ''', e=e)
    for unit in cursor:
        your_units.append([unit[0], unit[1], unit[2], unit[3], unit[4], unit[5], b64encode(unit[6].read()).decode("utf-8"), unit[7]])
    cursor.close()

    print(your_units)

    return render_template('your_units.html', your_units=your_units, x=x, y=y)


@app.route('/recruitunit', methods=["POST"])
def recruit_unit():
    user = session["user"]
    game_id = session["game_id"]
    unit_name = request.values['name']
    x = request.values['x']
    y = request.values['y']
    amount = request.values['amount']

    cursor = db.cursor()
    cursor.callproc("RecruitUnit_Action ", [unit_name, user, amount, x, y, int(game_id)])
    db.commit()

    cursor2 = db.cursor()
    resources_info = []
    objType = db.gettype("RESOURCES_INFO_TABLE")
    cursor2.execute(''' SELECT * FROM table(:a) ''', a=cursor.callfunc("get_resources_info", objType, [game_id, user]))
    for resource_info in cursor2:
        resources_info.append(list(resource_info))
    cursor2.close()

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]
    cursor.close()

    return render_template('resorces.html', resources_info=new_resourcer_info)


@app.route('/moveunit', methods=["POST"])
def move_unit():
    user = session["user"]
    game_id = session["game_id"]
    unit_name = request.values['name']
    source_x = request.values['x_source']
    source_y = request.values['y_source']
    dest_x = request.values['x_dest']
    dest_y = request.values['y_dest']

    cursor = db.cursor()
    cursor.callproc("MoveUnit", [user, unit_name, source_x, source_y, dest_x, dest_y, int(game_id)])
    db.commit()

    return "true"


if __name__ == '__main__':
    app.run()
