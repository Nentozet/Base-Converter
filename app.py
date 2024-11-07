import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, flash, get_flashed_messages, session
from program import Program
from user import User, db
from converter import Converter
from config import Config
from random import randint
import threading
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

program = Program()


def keep_alive():
    try:
        requests.get("https://base-converter.onrender.com/train")
    except Exception as e:
        print(f"Ошибка keep-alive: {e}")
    threading.Timer(10, keep_alive).start()


keep_alive()


@app.route("/", methods=["GET", "POST"])
@app.route("/converter", methods=["GET", "POST"])
def converter():
    program.init()

    if "user_id" in session:
        user_id = session.get("user_id")
        user = db.session.get(User, user_id)
        lang = user.language
    else:
        user = 0
        lang = session.get("language")

    if request.method == "POST":
        action = request.form.get("action")

        if not program.process_action(action, request, user):
            from_base = request.form.get("from_base")
            to_base = request.form.get("to_base")
            number_to_convert = request.form.get("number_to_convert")
            try:
                converted_number = Converter.get_converted_number(number_to_convert, int(from_base), int(to_base))
                session["conversion_result"] = converted_number
                session["color"] = Config.Right_Font_Color
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
    program.init()

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    user = db.session.get(User, user_id)

    if request.method == "POST":
        action = request.form.get("action")

        if program.process_action(action, request, user):
            flash("result_access_granted")

        return redirect(url_for("result"))

    return_page = session.get("return_page")
    if "result_access_granted" not in get_flashed_messages():
        return redirect(url_for(return_page))

    match return_page:
        case "converter":
            user_result = session.get("conversion_result")
        case "train":
            user_result = program.get_task_result(user)
        case _:
            raise Exception("Unknown source page")

    color = session.get("color")
    return_page = session.get("return_page")

    return program.get_rendered_template("result.html", user, user_result, color, return_page)


@app.route("/train", methods=["GET", "POST"])
def train():
    program.init()

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    user = db.session.get(User, user_id)

    if user.need_to_reset_task:
        program.reset_task(randint(1, 2), user)
        user.need_to_reset_task = False
        db.session.commit()

    if request.method == "POST":
        session["return_page"] = "train"

        action = request.form.get("action")
        if not program.process_action(action, request, user):
            flash("result_access_granted")

            answer = request.form.get("answer")

            user.need_to_reset_task = True
            db.session.commit()

            res = program.check_answer_for_task(answer, user)
            user.on_solved_task(res)

            return redirect(url_for("result"))

    print(user.task_correct_answers.split("|")[-1])

    task_text = program.get_task_text(user)
    return program.get_rendered_template("train.html", user, task_text)


@app.route("/register", methods=["GET", "POST"])
def register():
    program.init()

    if "user_id" in session:
        user_id = session.get("user_id")
        user = db.session.get(User, user_id)
        lang = user.language
    else:
        user = 0
        lang = session.get("language")

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

            print('sdfsdfs')

            new_user = User(username=username)
            new_user.set_password(password_1)
            new_user.language = session.get("language")
            new_user.theme = session.get("theme")
            print(new_user.language, new_user.language)

            db.session.add(new_user)
            db.session.commit()

            print('sdfsdfs')

            flash(program.Text_Base[lang]["registration_success"], "success")
            return redirect(url_for("login"))

    return program.get_rendered_template("register.html", user)


@app.route("/login", methods=["GET", "POST"])
def login():
    program.init()

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
                return redirect(url_for("train"))
            else:
                user = 0
                lang = session.get("language")
                flash(program.Text_Base[lang]["invalid_login_data"], "danger")

    return program.get_rendered_template("login.html", user)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)

    lang = session.get("language")
    text = program.Text_Base[lang]

    flash(text["logout_success"], "success")
    return redirect(url_for("login"))
    
