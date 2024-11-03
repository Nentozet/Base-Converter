from flask import Flask, request, redirect, url_for, flash, get_flashed_messages, session
from config import Config
from converter import Converter
from programm import Program
from user import User, db
from random import randint

app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

NEED_TO_RESET_TASK = True

program = Program(Config.Default_Language, Config.Default_Theme)


@app.route("/", methods=["GET", "POST"])
@app.route("/converter", methods=["GET", "POST"])
def converter():
    if "user_id" in session:
        user_id = session.get("user_id")
        user = db.session.get(User, user_id)
        lang = user.language
    else:
        user = 0
        lang = program.language

    if request.method == "POST":
        action = request.form.get("action")

        if not program.process_action(action, request, session, user):
            from_base = request.form.get("from_base")
            to_base = request.form.get("to_base")
            number_to_convert = request.form.get("number_to_convert")
            try:
                session["user_result"] = Converter.get_converted_number(number_to_convert, int(from_base), int(to_base))
                session["color"] = "#00b400"
                session["return_page"] = "converter"
                flash("result_access_granted")
                return redirect(url_for("result"))
            except ValueError:
                flash(program.Text_Base[lang]["convertion_error"], "danger")
                return redirect(url_for("converter"))

    messages = get_flashed_messages(with_categories=True)
    return program.get_rendered_template("converter.html", user, messages)


@app.route("/result", methods=["GET", "POST"])
def result():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    user = db.session.get(User, user_id)

    if request.method == "POST":
        action = request.form.get("action")

        if program.process_action(action, request, session):
            flash("result_access_granted")

        return redirect(url_for("result"))

    if "result_access_granted" not in get_flashed_messages():
        return_page = session.get("return_page")
        program.reset_task(1, user.language)
        return redirect(url_for(return_page))

    user_result = session.get("user_result")
    color = session.get("color")
    return_page = session.get("return_page")

    return program.get_rendered_template("result.html", user_result, color, return_page)


@app.route("/train", methods=["GET", "POST"])
def train():
    global NEED_TO_RESET_TASK

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    user = db.session.get(User, user_id)

    if NEED_TO_RESET_TASK:
        program.reset_task(randint(1, 2), user.language)
        NEED_TO_RESET_TASK = False

    if request.method == "POST":
        session["return_page"] = "train"

        action = request.form.get("action")
        if not program.process_action(action, request, session, user):
            flash("result_access_granted")

            answer = request.form.get("answer")
            res = program.check_answer_for_task(answer, session, user.language)
            user.on_solved_task(res)
            program.reset_task(randint(1, 2), user.language)
            return redirect(url_for("result"))

    task_text = program.task.text
    return program.get_rendered_template("train.html", user, task_text)


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        user_id = session.get("user_id")
        user = db.session.get(User, user_id)
        lang = user.language
    else:
        user = 0
        lang = program.language

    if request.method == "POST":
        action = request.form.get("action")
        if not program.process_action(action, request, session):
            username = request.form["username"]
            password_1 = request.form["password_1"]
            password_2 = request.form["password_2"]

            if User.query.filter_by(username=username).first():
                flash(program.Text_Base[lang]["repeated_username_alert"], "danger")
                return redirect(url_for("register"))

            if password_1 != password_2:
                flash(program.Text_Base[lang]["different_passwords_alert"], "danger")
                return redirect(url_for("register"))

            new_user = User(username=username)
            new_user.set_password(password_1)
            new_user.language = program.language
            new_user.theme = program.theme
            db.session.add(new_user)
            db.session.commit()

            flash(program.Text_Base[lang]["registration_success"], "success")
            return redirect(url_for("login"))

    return program.get_rendered_template("register.html", user)


@app.route("/login", methods=["GET", "POST"])
def login():
    global NEED_TO_RESET_TASK

    if "user_id" in session:
        return redirect(url_for("logout"))

    user = 0

    if request.method == "POST":
        action = request.form.get("action")
        if not program.process_action(action, request, session):
            username = request.form["username"]
            password = request.form["password"]

            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session["user_id"] = user.id
                # session["username"] = user.username
                NEED_TO_RESET_TASK = True
                return redirect(url_for("train"))
            else:
                flash(program.Text_Base[program.language]["invalid_login_data"], "danger")

    return program.get_rendered_template("login.html", user)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)

    lang = program.language
    text = program.Text_Base[lang]

    # get_flashed_messages()
    flash(text["logout_success"], "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1", threaded=True)
    # app.run(port=8080, host="0.0.0.0")
