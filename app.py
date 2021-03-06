from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from datetime import timedelta
import cx_Oracle
from base64 import b64encode

# cx_Oracle.init_oracle_client(lib_dir=r"D:\Program Files\OracleClient\instantclient_19_9")
cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\Szymon\Documents\instantclient_19_9")

app = Flask(__name__)
app.secret_key = "hoc1"
app.permanent_session_lifetime = timedelta(minutes=120)
# db = cx_Oracle.connect("inf141229", "inf141229", "admlab2.cs.put.poznan.pl/dblab02_students.cs.put.poznan.pl")


def connect_db():
    return cx_Oracle.connect("inf141229", "inf141229", "admlab2.cs.put.poznan.pl/dblab02_students.cs.put.poznan.pl")


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


def get_games_info(name):
    ids = []
    cursor = g.db.cursor()
    cursor.execute(''' SELECT game_id FROM users_in_games WHERE user_name = :usr_name ''', usr_name=name)
    for i in cursor:
        ids.append(i)
    infos = []
    cursor.close()

    G_INFO_TABLE = g.db.gettype("G_INFO_TABLE")
    NFULL_GAMES_TABLE = g.db.gettype("NFULL_GAMES_TABLE")

    cursor1 = g.db.cursor()
    for g_id in ids:
        cursor1.execute(''' SELECT * FROM table(:x)''', x=cursor1.callfunc('game_info', G_INFO_TABLE, [g_id[0]]))
        for y in cursor1:
            infos.append(list(y))
    cursor1.close()

    nfull = []
    cursor2 = g.db.cursor()
    cursor2.execute(''' SELECT * FROM table(:p) ''', p=cursor2.callfunc("nfull_games_info", NFULL_GAMES_TABLE, [name]))
    for rec in cursor2:
        nfull.append(list(rec))
    cursor2.close()

    return infos, nfull


def get_map(name, game_id):
    game_id = int(game_id)
    fields = []

    GAME_MAP_TABLE = g.db.gettype("GAME_MAP_TABLE")
    BUILDINGS_INFO_TABLE = g.db.gettype("BUILDINGS_INFO_TABLE")
    BUILDINGS_MAP_TABLE = g.db.gettype("BUILDINGS_MAP_TABLE")
    UNITS_MAP_TABLE = g.db.gettype("UNITS_MAP_TABLE")
    UNITS_INFO_TABLE = g.db.gettype("UNITS_INFO_TABLE")
    RESOURCES_INFO_TABLE = g.db.gettype("RESOURCES_INFO_TABLE")

    cursor3 = g.db.cursor()
    cursor3.execute(''' SELECT * FROM table(:z) ''', z=cursor3.callfunc("get_map", GAME_MAP_TABLE, [game_id]))
    for field in cursor3:
        fields.append(list(field))
    #print(fields)
    cursor3.close()

    cursor4 = g.db.cursor()
    buildings = []
    a = cursor4.callfunc("get_buildings_map", BUILDINGS_MAP_TABLE, [game_id])
    cursor4.close()
    cursor5 = g.db.cursor()
    cursor5.execute(''' SELECT * FROM table(:a) ''', a=a)
    for building in cursor5:
        buildings.append(list(building))
    #print(buildings)
    cursor5.close()

    cursor7 = g.db.cursor()
    units = []
    cursor7.execute(''' SELECT * FROM table(:b) ''', b=cursor7.callfunc("get_units_map", UNITS_MAP_TABLE, [game_id]))
    for unit in cursor7:
        units.append(list(unit))
    print(units)
    cursor7.close()

    cursor8 = g.db.cursor()
    units_info = []
    cursor8.execute(''' SELECT * FROM table(:x) ''', x=cursor8.callfunc("get_units_info", UNITS_INFO_TABLE, []))
    for unit_info in cursor8:
        units_info.append(list(unit_info))
    #print(units_info)
    cursor8.close()

    cursor9 = g.db.cursor()
    buildings_info = []
    cursor9.execute(''' SELECT * FROM table(:c) ''', c=cursor9.callfunc("get_buildings_info", BUILDINGS_INFO_TABLE, []))
    for building_info in cursor9:
        buildings_info.append(list(building_info))
    #print(buildings_info)
    cursor9.close()

    cursor10 = g.db.cursor()
    resources_info = []
    cursor10.execute(''' SELECT * FROM table(:d) ''', d=cursor10.callfunc("get_resources_info", RESOURCES_INFO_TABLE, [game_id, name]))
    for resource_info in cursor10:
        resources_info.append(list(resource_info))
    #print(resources_info)
    cursor10.close()

    return fields, buildings, units, units_info, buildings_info, resources_info


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login_page():
    return_msg = ""
    if request.method == 'POST':
        session.permanent = True
        user = request.form["nm"]
        password = request.form["pw"]
        try:
            cursor11 = g.db.cursor()
            cursor11.callfunc("goodPass", int, [user, password])
            session["user"] = user
            cursor11.close()

            cursor501 = g.db.cursor()
            if cursor501.callfunc("isAdmin", int, [user]) > 0:
                cursor501.close()
                return redirect(url_for("administration_panel"))
            else:
                cursor501.close()
                return redirect(url_for("user_page"))
        except Exception as e:
            print(e)
            return_msg = "Nieprawidłowe hasło lub login"
            return render_template('login_page.html', return_msg=return_msg)
    else:
        if "user" in session:
            return redirect(url_for("user_page"))
        return render_template('login_page.html', return_msg=return_msg)


@app.route('/register', methods=["POST", "GET"])
def register_page():
    return_msg = ""
    if request.method == 'POST':
        usr = request.form["nm"]
        usr_pw = request.form["pw"]
        usr_rpw = request.form["rpw"]
        if usr_rpw != usr_pw:
            return_msg = "Hasła nie są takie same."
            return render_template('register_page.html', return_msg=return_msg)
        else:
            cursor12 = g.db.cursor()
            if cursor12.callfunc("isRegistered", int, [usr]) > 0:
                return_msg = "Nazwa użytkownika jest już zajęta."
                cursor12.close()
                return render_template('register_page.html', return_msg=return_msg)
            else:
                cursor12.callproc("RegisterPlayer", [usr, usr_pw])
                g.db.commit()
                session.permanent = True
                session["user"] = usr
                cursor12.close()
                return redirect(url_for("user_page"))
    return render_template('register_page.html', return_msg=return_msg)


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
                cursor13 = g.db.cursor()
                cursor13.callproc("CreateGame", [user, int(x_size), int(y_size), int(max_players), float(r_chances)])
                g.db.commit()
                cursor13.close()
                return redirect(url_for("user_page"))
            else:
                return render_template("user_page.html", usr=user, games=infos, all_games=nfull)
        else:
            infos, nfull = get_games_info(user)
            return render_template("user_page.html", usr=user, games=infos, all_games=nfull)
    else:
        return redirect(url_for("login_page"))


@app.route('/user/addToGame/<game_id>')
def add_to_game(game_id):
    user = session["user"]
    cursor500 = g.db.cursor()
    cursor500.callproc("AddPlayerToGame", [user, game_id])
    cursor500.close()
    return redirect(url_for("game", game_id=game_id))


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

    cursor14 = g.db.cursor()
    o = cursor14.callfunc("get_turn", int, [game_id])
    cursor14.close()

    return render_template('game.html', user_name=user, width=width, height=height, fields=fields, buildings=new_buildings, units=new_units, units_info=new_units_info, buildings_info=new_buildings_info, resources_info=new_resourcer_info, turn_number=o)


@app.route('/getturn', methods=["POST"])
def get_turn():
    game_id = session["game_id"]
    cursor15 = g.db.cursor()
    p = cursor15.callfunc("get_turn", int, [game_id])
    cursor15.close()

    return str(p)

@app.route('/nextturn', methods=["POST"])
def next_turn():
    game_id = session["game_id"]
    user = session["user"]
    cursor16 = g.db.cursor()
    cursor16.callproc("nextTurn", [game_id, user])
    cursor16.close()

    return "True"


@app.route('/science', methods=["POST"])
def science():
    user = session["user"]
    game_id = session["game_id"]

    science = []
    cursor17 = g.db.cursor()

    SCIENCE_INFO_TABLE = g.db.gettype("SCIENCE_INFO_TABLE")
    RESOURCES_INFO_TABLE = g.db.gettype("RESOURCES_INFO_TABLE")

    h = cursor17.callfunc("get_available_science", SCIENCE_INFO_TABLE, [game_id, user])
    cursor17.close()
    cursor18 = g.db.cursor()
    cursor18.execute(''' SELECT * FROM table(:h) ''', h=h)
    for s in cursor18:
        cursor19 = g.db.cursor()
        cursor19.execute(''' SELECT * FROM table(:l) ''', l=s[5])
        res = []
        for r in cursor19:
            res.append(r)
        science.append([s[0], s[1], b64encode(s[2].read()).decode("utf-8"), s[3], s[4], res])
        cursor19.close()

    cursor20 = g.db.cursor()
    resources_info = []
    cursor20.execute(''' SELECT * FROM table(:ar) ''', ar=cursor20.callfunc("get_resources_info", RESOURCES_INFO_TABLE, [game_id, user]))
    for resource_info in cursor20:
        resources_info.append(list(resource_info))

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]
    cursor20.close()

    return render_template('science.html', science=science, resources_info=new_resourcer_info)


@app.route('/doscience', methods=["POST"])
def do_science():
    user = session["user"]
    game_id = session["game_id"]
    science_name = request.values['name']

    RESOURCES_INFO_TABLE = g.db.gettype("RESOURCES_INFO_TABLE")

    cursor21 = g.db.cursor()
    cursor21.callproc("doScience", [int(game_id), user, science_name])
    cursor21.close()

    cursor22 = g.db.cursor()
    resources_info = []
    cursor22.execute(''' SELECT * FROM table(:a) ''', a=cursor22.callfunc("get_resources_info", RESOURCES_INFO_TABLE, [game_id, user]))
    for resource_info in cursor22:
        resources_info.append(list(resource_info))
    cursor22.close()

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]

    return render_template('resorces.html', resources_info=new_resourcer_info)


@app.route('/availablebuildings', methods=["POST"])
def available_buildings():
    user = session["user"]
    game_id = session["game_id"]
    x = request.values['x']
    y = request.values['y']

    AVAILABLE_BUILDINGS_TABLE = g.db.gettype("AVAILABLE_BUILDINGS_TABLE")
    RESOURCES_INFO_TABLE = g.db.gettype("RESOURCES_INFO_TABLE")

    available_buildings = []
    cursor23 = g.db.cursor()
    h = cursor23.callfunc("get_available_buildings", AVAILABLE_BUILDINGS_TABLE, [game_id, user, x, y])
    cursor23.close()
    cursor24 = g.db.cursor()
    cursor24.execute(''' SELECT * FROM table(:h) ''', h=h)
    for building in cursor24:
        cursor25 = g.db.cursor()
        cursor25.execute(''' SELECT * FROM table(:l) ''', l=building[5])
        costs = []
        for r in cursor25:
            costs.append(r)
        cursor25.close()

        cursor26 = g.db.cursor()
        cursor26.execute(''' SELECT * FROM table(:i) ''', i=building[6])
        income = []
        for r in cursor26:
            income.append(r)
        cursor26.close()

        available_buildings.append([building[0], building[1], b64encode(building[2].read()).decode("utf-8"), building[3], building[4], costs, income])
    cursor24.close()

    cursor27 = g.db.cursor()
    resources_info = []
    cursor27.execute(''' SELECT * FROM table(:r) ''', r=cursor27.callfunc("get_resources_info", RESOURCES_INFO_TABLE, [game_id, user]))
    for resource_info in cursor27:
        resources_info.append(list(resource_info))

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]
    cursor27.close()

    return render_template('available_buildings.html', available_buildings=available_buildings, resources_info=new_resourcer_info, x=x, y=y)


@app.route('/yourbuildings', methods=["POST"])
def your_buildings():
    user = session["user"]
    game_id = session["game_id"]
    x = request.values['x']
    y = request.values['y']

    YOUR_BUILDINGS_TABLE = g.db.gettype("YOUR_BUILDINGS_TABLE")
    RESOURCES_INFO_TABLE = g.db.gettype("RESOURCES_INFO_TABLE")

    your_buildings = []
    cursor28 = g.db.cursor()
    v = cursor28.callfunc("get_your_buildings", YOUR_BUILDINGS_TABLE, [game_id, user, x, y])
    cursor28.close()
    cursor29 = g.db.cursor()
    cursor29.execute(''' SELECT * FROM table(:v) ''', v=v)
    for building in cursor29:
        cursor30 = g.db.cursor()
        cursor30.execute(''' SELECT * FROM table(:l) ''', l=building[3])
        income = []
        for r in cursor30:
            income.append(r)
        cursor30.close()

        your_buildings.append([building[0], b64encode(building[1].read()).decode("utf-8"), building[2], income])
    cursor29.close()

    cursor31 = g.db.cursor()
    resources_info = []
    cursor31.execute(''' SELECT * FROM table(:r) ''', r=cursor31.callfunc("get_resources_info", RESOURCES_INFO_TABLE, [game_id, user]))
    for resource_info in cursor31:
        resources_info.append(list(resource_info))
    cursor31.close()

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]

    print(your_buildings)

    return render_template('your_buildings.html', your_buildings=your_buildings, resources_info=new_resourcer_info, x=x, y=y)


@app.route('/buildbuilding', methods=["POST"])
def build_building():
    user = session["user"]
    game_id = session["game_id"]
    building_name = request.values['name']
    x = request.values['x']
    y = request.values['y']

    RESOURCES_INFO_TABLE = g.db.gettype("RESOURCES_INFO_TABLE")

    cursor32 = g.db.cursor()
    cursor32.callproc("BuildBuilding", [int(game_id), x, y, building_name, user])
    cursor32.close()

    cursor33 = g.db.cursor()
    resources_info = []
    cursor33.execute(''' SELECT * FROM table(:a) ''', a=cursor33.callfunc("get_resources_info", RESOURCES_INFO_TABLE, [game_id, user]))
    for resource_info in cursor33:
        resources_info.append(list(resource_info))
    cursor33.close()

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]

    return render_template('resorces.html', resources_info=new_resourcer_info)


@app.route('/availableunits', methods=["POST"])
def available_units():
    user = session["user"]
    game_id = session["game_id"]
    x = request.values['x']
    y = request.values['y']

    AVAILABLE_UNIT_TABLE = g.db.gettype("AVAILABLE_UNIT_TABLE")
    RESOURCES_INFO_TABLE = g.db.gettype("RESOURCES_INFO_TABLE")

    available_units = []
    cursor34 = g.db.cursor()
    f = cursor34.callfunc("get_available_units", AVAILABLE_UNIT_TABLE, [game_id, user, x, y])
    cursor34.close()
    cursor35 = g.db.cursor()
    cursor35.execute(''' SELECT * FROM table(:f) ''', f=f)
    for unit in cursor35:
        cursor36 = g.db.cursor()
        cursor36.execute(''' SELECT * FROM table(:l) ''', l=unit[9])
        costs = []
        for r in cursor36:
            costs.append(r)
        cursor36.close()

        available_units.append([unit[0], unit[1], unit[2], unit[3], unit[4], unit[5], b64encode(unit[6].read()).decode("utf-8"), unit[7], unit[8], costs])
    cursor35.close()

    cursor37 = g.db.cursor()
    resources_info = []
    cursor37.execute(''' SELECT * FROM table(:r) ''', r=cursor37.callfunc("get_resources_info", RESOURCES_INFO_TABLE, [game_id, user]))
    for resource_info in cursor37:
        resources_info.append(list(resource_info))

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]
    cursor37.close()

    print(available_units)

    return render_template('available_units.html', available_units=available_units, resources_info=new_resourcer_info, x=x, y=y)


@app.route('/yourunits', methods=["POST"])
def your_units():
    user = session["user"]
    game_id = session["game_id"]
    x = request.values['x']
    y = request.values['y']

    YOUR_UNITS_TABLE = g.db.gettype("YOUR_UNITS_TABLE")

    your_units = []
    cursor38 = g.db.cursor()
    e = cursor38.callfunc("get_your_units", YOUR_UNITS_TABLE, [game_id, user, x, y])
    cursor38.close()
    cursor39 = g.db.cursor()
    cursor39.execute(''' SELECT * FROM table(:e) ''', e=e)
    for unit in cursor39:
        your_units.append([unit[0], unit[1], unit[2], unit[3], unit[4], unit[5], b64encode(unit[6].read()).decode("utf-8"), unit[7]])
    cursor39.close()

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

    RESOURCES_INFO_TABLE = g.db.gettype("RESOURCES_INFO_TABLE")

    cursor40 = g.db.cursor()
    cursor40.callproc("RecruitUnit_Action ", [unit_name, user, amount, x, y, int(game_id)])
    cursor40.close()

    cursor41 = g.db.cursor()
    resources_info = []
    cursor41.execute(''' SELECT * FROM table(:a) ''', a=cursor41.callfunc("get_resources_info", RESOURCES_INFO_TABLE, [game_id, user]))
    for resource_info in cursor41:
        resources_info.append(list(resource_info))
    cursor41.close()

    new_resourcer_info = dict()
    for i in resources_info:
        new_resourcer_info[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]

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

    try:
        cursor42 = g.db.cursor()
        cursor42.callproc("MoveUnit", [user, unit_name, source_x, source_y, dest_x, dest_y, int(game_id)])
        cursor42.close()
    except:
        print("move_unit")
    return "true"


@app.route('/administrationpanel', methods=["GET"])
def administration_panel():
    user = session["user"]
    return render_template("administration_panel.html", usr=user)


def get_select_lists3():
    buildings_name = []
    cursor_b = g.db.cursor()
    cursor_b.execute(''' SELECT NAME FROM BUILDINGS''')
    for i in cursor_b:
        buildings_name.append(i[0])
    cursor_b.close()

    science_name = []
    cursor_s = g.db.cursor()
    cursor_s.execute(''' SELECT NAME FROM SCIENCE''')
    for i in cursor_s:
        science_name.append(i[0])
    cursor_s.close()

    resources_name = []
    cursor_r = g.db.cursor()
    cursor_r.execute(''' SELECT NAME FROM RESOURCES''')
    for i in cursor_r:
        resources_name.append(i[0])
    cursor_r.close()

    return buildings_name, science_name, resources_name


def get_select_lists2():
    buildings_name = []
    cursor_b = g.db.cursor()
    cursor_b.execute(''' SELECT NAME FROM BUILDINGS''')
    for i in cursor_b:
        buildings_name.append(i[0])
    cursor_b.close()

    science_name = []
    cursor_s = g.db.cursor()
    cursor_s.execute(''' SELECT NAME FROM SCIENCE''')
    for i in cursor_s:
        science_name.append(i[0])
    cursor_s.close()

    return buildings_name, science_name


@app.route('/administrationpanel/buildings', methods=["GET", "POST"])
def administration_panel_buildings():
    user = session["user"]
    buildings_array = []
    cursor100 = g.db.cursor()
    cursor100.execute(''' select b.NAME, ICON, DESCRIPTION, REQUIRED_SCIENCE, REQUIRED_BUILDING, TURNS_TO_MAKE,  REQUIRED_RESOURCE
                        from BUILDINGS b left join MINES m on b.NAME = m.NAME ''')
    for i in cursor100:
        buildings_array.append(i)
    cursor100.close()

    buildings_array2 = dict()
    for i in buildings_array:
        buildings_array2[i[0]] = [i[5], i[2], i[3], i[4], i[6], b64encode(i[1].read()).decode("utf-8")]

    buildings_name, science_name, resources_name = get_select_lists3()

    if request.method == 'POST':
        b_name = request.form["b_name"]
        b_turns = request.form["b_turns"]
        b_desc = request.form["b_desc"]
        b_s_req = request.form["b_s_req"]
        b_b_req = request.form["b_b_req"]
        b_r_req = request.form["b_r_req"]
        b_icon = request.form["b_icon"]
        if b_icon == "":
            b_icon = None
        if b_desc == "":
            b_desc = None
        if b_s_req == "":
            b_s_req = None
        if b_b_req == "":
            b_b_req = None
        if b_r_req == "":
            b_r_req = None

        try:
            if b_icon is not None:
                with open(f"static/images/{b_icon}", 'rb') as f:
                    img = f.read()
            else:
                with open(f"static/images/castle_tab.png", 'rb') as f:
                    img = f.read()
            cursor101 = g.db.cursor()
            cursor101.callproc("AddBuilding", [b_name, img, b_desc, b_turns, b_s_req, b_b_req])
            cursor101.close()
            if b_r_req is not None:
                cursor201 = g.db.cursor()
                cursor201.callproc("AddToMines", [b_name, b_r_req])
                cursor201.close()
        except:
            print("Add_building")

        return redirect(url_for("administration_panel_buildings"))
    else:
        return render_template("administration_panel_buildings.html", usr=user, b_array=buildings_array2,
                               buildings_name=buildings_name, science_name=science_name, resources_name=resources_name)


@app.route('/administrationpanel/buildings/delete/<b_name>', methods=['GET'])
def delete_building(b_name):
    try:
        print(b_name)
        cursor102 = g.db.cursor()
        cursor102.callproc('RemoveBuilding', [b_name])
        cursor102.close()
        return redirect(url_for("administration_panel_buildings"))
    except:
        print("delete_building")
        return redirect(url_for("administration_panel_buildings"))


@app.route('/administrationpanel/resources', methods=["GET", "POST"])
def administration_panel_resources():
    user = session["user"]
    resources_array = []
    cursor103 = g.db.cursor()
    cursor103.execute(''' SELECT * FROM RESOURCES ''')
    for i in cursor103:
        resources_array.append(i)
    cursor103.close()

    resources_array2 = dict()
    for i in resources_array:
        resources_array2[i[0]] = [i[2], b64encode(i[1].read()).decode("utf-8")]

    if request.method == 'POST':
        r_name = request.form["r_name"]
        r_desc = request.form["r_desc"]
        r_icon = request.form["r_icon"]
        if r_icon == "":
            r_icon = None
        if r_desc == "":
            r_desc = None
        try:
            if r_icon is not None:
                with open(f"static/images/{r_icon}", 'rb') as f:
                    img = f.read()
            else:
                with open(f"static/images/gold-ingots.png", 'rb') as f:
                    img = f.read()
            cursor104 = g.db.cursor()
            cursor104.callproc("AddResource", [r_name, img, r_desc])
            cursor104.close()
        except:
            print("Add_resource")
        return redirect(url_for("administration_panel_resources"))
    else:
        return render_template("administration_panel_resources.html", usr=user, res_array=resources_array2)


@app.route('/administrationpanel/resources/delete/<r_name>', methods=['GET'])
def delete_resource(r_name):
    try:
        print(r_name)
        cursor105 = g.db.cursor()
        cursor105.callproc('RemoveResource', [r_name])
        cursor105.close()
        print(r_name)
        return redirect(url_for("administration_panel_resources"))
    except:
        print("delete_resource")
        return redirect(url_for("administration_panel_resources"))


@app.route('/administrationpanel/science', methods=["GET", "POST"])
def administration_panel_science():
    user = session["user"]
    science_array = []
    cursor106 = g.db.cursor()
    cursor106.execute(''' SELECT * FROM SCIENCE ''')
    for i in cursor106:
        science_array.append(i)
    cursor106.close()

    science_array2 = dict()
    for i in science_array:
        science_array2[i[0]] = [i[5], i[2], i[3], i[4], b64encode(i[1].read()).decode("utf-8")]

    buildings_name, science_name = get_select_lists2()

    if request.method == 'POST':
        s_name = request.form["s_name"]
        s_turns = request.form["s_turns"]
        s_desc = request.form["s_desc"]
        s_s_req = request.form["s_s_req"]
        s_b_req = request.form["s_b_req"]
        s_icon = request.form["s_icon"]
        if s_icon == "":
            s_icon = None
        if s_desc == "":
            s_desc = None
        if s_s_req == "":
            s_s_req = None
        if s_b_req == "":
            s_b_req = None

        try:
            if s_icon is not None:
                with open(f"static/images/{s_icon}", 'rb') as f:
                    img = f.read()
            else:
                with open(f"static/images/chemistry.png", 'rb') as f:
                    img = f.read()
            cursor107 = g.db.cursor()
            cursor107.callproc("AddScience", [s_name, img, s_desc, s_turns, s_s_req, s_b_req])
            cursor107.close()
        except:
            print("Add_science")
        return redirect(url_for("administration_panel_science"))
    else:
        return render_template("administration_panel_science.html", usr=user, sc_array=science_array2,
                               buildings_name=buildings_name, science_name=science_name)


@app.route('/administrationpanel/science/delete/<s_name>', methods=['GET'])
def delete_science(s_name):
    try:
        print(s_name)
        cursor108 = g.db.cursor()
        cursor108.callproc('RemoveScience', [s_name])
        cursor108.close()
        return redirect(url_for("administration_panel_science"))
    except:
        print("delete_science")
        return redirect(url_for("administration_panel_science"))


@app.route('/administrationpanel/units', methods=["GET", "POST"])
def administration_panel_units():
    user = session["user"]
    units_array = []
    cursor109 = g.db.cursor()
    cursor109.execute(''' SELECT * FROM UNITS ''')
    for i in cursor109:
        units_array.append(i)
    cursor109.close()

    units_array2 = dict()
    for i in units_array:
        units_array2[i[0]] = [i[1], i[2], i[4], i[3], i[9], i[6], i[7], i[8], b64encode(i[5].read()).decode("utf-8")]

    buildings_name, science_name = get_select_lists2()

    if request.method == 'POST':
        u_name = request.form["u_name"]
        u_damage = request.form["u_damage"]
        u_def = request.form["u_def"]
        u_hp = request.form["u_hp"]
        u_traveldist = request.form["u_traveldist"]
        u_turns = request.form["u_turns"]
        u_desc = request.form["u_desc"]
        u_s_req = request.form["u_s_req"]
        u_b_req = request.form["u_b_req"]
        u_icon = request.form["u_icon"]
        if u_icon == "":
            u_icon = None
        if u_desc == "":
            u_desc = None
        if u_s_req == "":
            u_s_req = None
        if u_b_req == "":
            u_b_req = None

        try:
            if u_icon is not None:
                with open(f"static/images/{u_icon}", 'rb') as f:
                    img = f.read()
            else:
                with open(f"static/images/axes.png", 'rb') as f:
                    img = f.read()
            cursor110 = g.db.cursor()
            cursor110.callproc("AddUnit", [u_name, u_damage, u_def, u_traveldist, u_hp, img, u_desc, u_turns, u_s_req, u_b_req])
            cursor110.close()
        except:
            print("Add_unit")
        return redirect(url_for("administration_panel_units"))
    else:
        return render_template("administration_panel_units.html", usr=user, u_array=units_array2,
                               buildings_name=buildings_name, science_name=science_name)


@app.route('/administrationpanel/units/delete/<u_name>', methods=['GET'])
def delete_unit(u_name):
    try:
        print(u_name)
        cursor111 = g.db.cursor()
        cursor111.callproc('RemoveUnit', [u_name])
        cursor111.close()
        return redirect(url_for("administration_panel_units"))
    except:
        print("delete_unit")
        return redirect(url_for("administration_panel_units"))


@app.route('/administrationpanel/resources/update/<r_name>', methods=["GET", "POST"])
def administration_panel_update_resource(r_name):
    user = session["user"]
    resource_info = []
    cursor112 = g.db.cursor()
    cursor112.execute(''' SELECT * FROM RESOURCES WHERE NAME = :ab ''', ab=r_name)
    for i in cursor112:
        resource_info.append(i)
    cursor112.close()
    print(resource_info)

    resource_info2 = dict()
    for i in resource_info:
        resource_info2[i[0]] = [i[2], b64encode(i[1].read()).decode("utf-8")]

    if request.method == 'POST':
        r_name = request.form["r_name"]
        r_desc = request.form["r_desc"]
        r_icon = request.form["r_icon"]
        print(r_icon)
        if r_icon == "":
            r_icon = None
        if r_desc == "":
            r_desc = None

        print(r_icon)
        if r_icon is not None:
            with open(f"static/images/{r_icon}", 'rb') as f:
                img = f.read()
        else:
            img = resource_info[0][1]
        cursor113 = g.db.cursor()
        cursor113.callproc("UpdateResource", [r_name, img, r_desc])
        cursor113.close()
        return redirect(url_for("administration_panel_resources"))
    else:
        return render_template("administration_panel_update_resource.html", usr=user, name=r_name, resource=resource_info2)


@app.route('/administrationpanel/science/update/<s_name>', methods=["GET", "POST"])
def administration_panel_update_science(s_name):
    user = session["user"]
    science_info = []
    cursor114 = g.db.cursor()
    cursor114.execute(''' SELECT * FROM SCIENCE WHERE NAME = :ac ''', ac=s_name)
    for i in cursor114:
        science_info.append(i)
    cursor114.close()

    science_info2 = dict()
    for i in science_info:
        science_info2[i[0]] = [i[5], i[2], i[3], i[4], b64encode(i[1].read()).decode("utf-8")]

    cost_array = []
    cursor115 = g.db.cursor()
    cursor115.execute(''' SELECT RESOURCE_NAME, AMOUNT, ICON 
                        from SCIENCE_COSTS S join RESOURCES R on S.RESOURCE_NAME = R.NAME
                         WHERE SCIENCE_NAME = :ad ''', ad=s_name)
    for i in cursor115:
        cost_array.append(i)
    cursor115.close()

    cost_array2 = dict()
    for i in cost_array:
        cost_array2[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]

    buildings_name, science_name, resources_name = get_select_lists3()

    if request.method == 'POST':
        science_name = request.form["science_name"]
        if science_name != "":
            return redirect(url_for("add_science_cost", s_name=science_name, r_name=request.form["r_name"],
                                    r_amount=request.form["r_amount"]))

        s_name = request.form["s_name"]
        s_turns = request.form["s_turns"]
        s_desc = request.form["s_desc"]
        s_s_req = request.form["s_s_req"]
        s_b_req = request.form["s_b_req"]
        s_icon = request.form["s_icon"]
        if s_icon == "":
            s_icon = None
        if s_desc == "":
            s_desc = None
        if s_s_req == "":
            s_s_req = None
        if s_b_req == "":
            s_b_req = None

        try:
            if s_icon is not None:
                with open(f"static/images/{s_icon}", 'rb') as f:
                    img = f.read()
            else:
                img = science_info[0][1]
            cursor116 = g.db.cursor()
            cursor116.callproc("UpdateScience", [s_name, img, s_desc, s_turns, s_s_req, s_b_req])
            cursor116.close()
        except:
            print("Update_science")
        return redirect(url_for("administration_panel_science"))
    else:
        return render_template("administration_panel_update_science.html", usr=user, name=s_name, science=science_info2,
                               cost=cost_array2, buildings_name=buildings_name, science_name=science_name, resources_name=resources_name)


@app.route('/administrationpanel/science/update/<s_name>/addCost/<r_name>/<r_amount>', methods=['GET'])
def add_science_cost(s_name, r_name, r_amount):
    try:
        cursor117 = g.db.cursor()
        cursor117.callproc('AddCostToScience', [s_name, r_name, r_amount])
        cursor117.close()
    except:
        print("delete_science_cost")
    return redirect(url_for("administration_panel_update_science", s_name=s_name))


@app.route('/administrationpanel/science/update/<s_name>/delCost/<r_name>', methods=['GET'])
def delete_science_cost(s_name, r_name):
    try:
        cursor118 = g.db.cursor()
        cursor118.callproc('RemoveCostFromScience', [s_name, r_name])
        cursor118.close()
    except:
        print("delete_science_cost")
    return redirect(url_for("administration_panel_update_science", s_name=s_name))


@app.route('/administrationpanel/units/update/<u_name>', methods=["GET", "POST"])
def administration_panel_update_unit(u_name):
    user = session["user"]
    unit_info = []
    cursor119 = g.db.cursor()
    cursor119.execute(''' SELECT * FROM UNITS WHERE NAME = :ae ''', ae=u_name)
    for i in cursor119:
        unit_info.append(i)
    cursor119.close()

    unit_info2 = dict()
    for i in unit_info:
        unit_info2[i[0]] = [i[1], i[2], i[4], i[3], i[9], i[6], i[7], i[8], b64encode(i[5].read()).decode("utf-8")]

    cost_array = []
    cursor120 = g.db.cursor()
    cursor120.execute(''' SELECT RESOURCE_NAME, AMOUNT, ICON 
                            from UNITS_COSTS S join RESOURCES R on S.RESOURCE_NAME = R.NAME
                             WHERE UNIT_NAME = :af ''', af=u_name)
    for i in cursor120:
        cost_array.append(i)
    cursor120.close()

    cost_array2 = dict()
    for i in cost_array:
        cost_array2[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]

    buildings_name, science_name, resources_name = get_select_lists3()

    if request.method == 'POST':
        unit_name = request.form["unit_name"]
        print(unit_name)
        if unit_name != "":
            return redirect(url_for("add_unit_cost", u_name=unit_name, r_name=request.form["r_name"],
                                    r_amount=request.form["r_amount"]))

        u_name = request.form["u_name"]
        u_damage = request.form["u_damage"]
        u_def = request.form["u_def"]
        u_hp = request.form["u_hp"]
        u_traveldist = request.form["u_traveldist"]
        u_turns = request.form["u_turns"]
        u_desc = request.form["u_desc"]
        u_s_req = request.form["u_s_req"]
        u_b_req = request.form["u_b_req"]
        u_icon = request.form["u_icon"]
        if u_icon == "":
            u_icon = None
        if u_desc == "":
            u_desc = None
        if u_s_req == "":
            u_s_req = None
        if u_b_req == "":
            u_b_req = None

        try:
            if u_icon is not None:
                with open(f"static/images/{u_icon}", 'rb') as f:
                    img = f.read()
            else:
                img = unit_info[0][5]
            cursor121 = g.db.cursor()
            cursor121.callproc("UpdateUnit", [u_name, u_damage, u_def, u_traveldist, u_hp, img, u_desc, u_turns, u_s_req, u_b_req])
            cursor121.close()
        except:
            print("Update_unit")

        return redirect(url_for("administration_panel_units"))
    else:
        return render_template("administration_panel_update_unit.html", usr=user, name=u_name, u_array=unit_info2, cost=cost_array2,
                               buildings_name=buildings_name, science_name=science_name, resources_name=resources_name)


@app.route('/administrationpanel/units/update/<u_name>/addCost/<r_name>/<r_amount>', methods=['GET'])
def add_unit_cost(u_name, r_name, r_amount):
    try:
        cursor122 = g.db.cursor()
        cursor122.callproc('AddCostToUnit', [u_name, r_name, r_amount])
        cursor122.close()
    except:
        print("add_unit_cost")
    return redirect(url_for("administration_panel_update_unit", u_name=u_name))


@app.route('/administrationpanel/units/update/<u_name>/delCost/<r_name>', methods=['GET'])
def delete_unit_cost(u_name, r_name):
    try:
        cursor123 = g.db.cursor()
        cursor123.callproc('RemoveCostFromUnit', [u_name, r_name])
        cursor123.close()
    except:
        print("delete_unit_cost")
    return redirect(url_for("administration_panel_update_unit", u_name=u_name))


@app.route('/administrationpanel/buildings/update/<b_name>', methods=["GET", "POST"])
def administration_panel_update_building(b_name):
    user = session["user"]
    building_info = []
    cursor124 = g.db.cursor()
    cursor124.execute(''' select b.NAME, ICON, DESCRIPTION, REQUIRED_SCIENCE, REQUIRED_BUILDING, TURNS_TO_MAKE,  REQUIRED_RESOURCE
                        from BUILDINGS b left join MINES m on b.NAME = m.NAME
                         WHERE b.NAME = :ag ''', ag=b_name)
    for i in cursor124:
        building_info.append(i)
    cursor124.close()

    building_info2 = dict()
    for i in building_info:
        building_info2[i[0]] = [i[5], i[2], i[3], i[4], i[6], b64encode(i[1].read()).decode("utf-8")]

    print(building_info)

    cost_array = []
    cursor125 = g.db.cursor()
    cursor125.execute(''' SELECT RESOURCE_NAME, AMOUNT, ICON 
                                from BUILDINGS_COSTS S join RESOURCES R on S.RESOURCE_NAME = R.NAME
                                 WHERE BUILDING_NAME = :ah ''', ah=b_name)
    for i in cursor125:
        cost_array.append(i)
    cursor125.close()

    cost_array2 = dict()
    for i in cost_array:
        cost_array2[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]

    incomes_array = []
    cursor126 = g.db.cursor()
    cursor126.execute(''' SELECT RESOURCE_NAME, AMOUNT, ICON 
                                   from BUILDINGS_INCOMES S join RESOURCES R on S.RESOURCE_NAME = R.NAME
                                    WHERE BUILDING_NAME = :ah ''', ah=b_name)
    for i in cursor126:
        incomes_array.append(i)
    cursor126.close()

    incomes_array2 = dict()
    for i in incomes_array:
        incomes_array2[i[0]] = [i[1], b64encode(i[2].read()).decode("utf-8")]

    buildings_name, science_name, resources_name = get_select_lists3()

    if request.method == 'POST':
        building_name = request.form["building_name"]
        if building_name != "":
            if building_name[-1] == "1":
                return redirect(url_for("add_building_cost", b_name=building_name[:-1], r_name=request.form["r_name"],
                                        r_amount=request.form["r_amount"]))
            elif building_name[-1] == "2":
                return redirect(url_for("add_building_income", b_name=building_name[:-1], r_name=request.form["r_name"],
                                        r_amount=request.form["r_amount"]))

        b_name = request.form["b_name"]
        b_turns = request.form["b_turns"]
        b_desc = request.form["b_desc"]
        b_s_req = request.form["b_s_req"]
        b_b_req = request.form["b_b_req"]
        b_r_req = request.form["b_r_req"]
        b_icon = request.form["b_icon"]
        if b_icon == "":
            b_icon = None
        if b_desc == "":
            b_desc = None
        if b_s_req == "":
            b_s_req = None
        if b_b_req == "":
            b_b_req = None
        if b_r_req == "":
            b_r_req = None

        try:
            if b_icon is not None:
                with open(f"static/images/{b_icon}", 'rb') as f:
                    img = f.read()
            else:
                img = building_info[0][1]

            cursor127 = g.db.cursor()
            cursor127.callproc("UpdateBuilding", [b_name, img, b_desc, b_turns, b_s_req, b_b_req])
            cursor127.close()

            if b_r_req is None and building_info[0][6] is not None:
                cursor227 = g.db.cursor()
                cursor227.callproc("RemoveFromMines", [b_name])
                cursor227.close()
            elif b_r_req is not None and building_info[0][6] is None:
                cursor327 = g.db.cursor()
                cursor327.callproc("AddToMines", [b_name, b_r_req])
                cursor327.close()
            elif b_r_req is not None and building_info[0][6] is not None:
                cursor427 = g.db.cursor()
                cursor427.callproc("UpdateMine", [b_name, b_r_req])
                cursor427.close()
        except:
            print("Update_building")
        return redirect(url_for("administration_panel_buildings"))
    else:
        return render_template("administration_panel_update_building.html", usr=user, name=b_name,
                               b_array=building_info2, cost=cost_array2, incomes=incomes_array2,
                               buildings_name=buildings_name, science_name=science_name, resources_name=resources_name)


@app.route('/administrationpanel/buildings/update/<b_name>/addCost/<r_name>/<r_amount>', methods=['GET'])
def add_building_cost(b_name, r_name, r_amount):
    try:
        cursor128 = g.db.cursor()
        cursor128.callproc('AddCostToBuilding', [b_name, r_name, r_amount])
        cursor128.close()
    except:
        print("add_building_cost")
    return redirect(url_for("administration_panel_update_building", b_name=b_name))


@app.route('/administrationpanel/buildings/update/<b_name>/delCost/<r_name>', methods=['GET'])
def delete_building_cost(b_name, r_name):
    try:
        cursor129 = g.db.cursor()
        cursor129.callproc('RemoveCostFromBuilding', [b_name, r_name])
        cursor129.close()
    except:
        print("delete_building_cost")
    return redirect(url_for("administration_panel_update_building", b_name=b_name))


@app.route('/administrationpanel/buildings/update/<b_name>/addIncome/<r_name>/<r_amount>', methods=['GET'])
def add_building_income(b_name, r_name, r_amount):
    try:
        cursor130 = g.db.cursor()
        cursor130.callproc('AddIncomeToBuilding', [b_name, r_name, r_amount])
        cursor130.close()
    except:
        print("add_building_income")
    return redirect(url_for("administration_panel_update_building", b_name=b_name))


@app.route('/administrationpanel/buildings/update/<b_name>/delIncome/<r_name>', methods=['GET'])
def delete_building_income(b_name, r_name):
    try:
        cursor131 = g.db.cursor()
        cursor131.callproc('RemoveIncomeFromBuilding', [b_name, r_name])
        cursor131.close()
    except:
        print("delete_building_income")
    return redirect(url_for("administration_panel_update_building", b_name=b_name))


if __name__ == '__main__':
    app.run()
