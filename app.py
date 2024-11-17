import os
from flask import Flask, request, redirect, url_for, flash, get_flashed_messages, session
from converter import Converter
from config import Config
from program import Program
from random import randint
from user import User, db
from toolset import Toolset
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

program = Program()

Toolset.keep_alive()


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
                session["result"] = converted_number
                session["color"] = Config.Correct_Font_Color
                session["return_page"] = "converter"
                flash("result_access_granted")
                return redirect(url_for("result"))
            except ValueError:
                flash(program.Text_Base[lang]["convertion_error"], "danger")
                return redirect(url_for("converter"))

    converter_checked = "checked"
    return program.get_rendered_template("converter.html", user, converter_checked)


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    program.init()

    if "user_id" in session:
        user_id = session.get("user_id")
        user = db.session.get(User, user_id)
        lang = user.language
    else:
        user = 0
        lang = session.get("language")

    if request.method == "POST":
        session["return_page"] = "calculator"

        action = request.form.get("action")
        if not program.process_action(action, request, user):
            number1 = request.form.get("number1")
            base1 = request.form.get("base1")
            number2 = request.form.get("number2")
            base2 = request.form.get("base2")
            operation = request.form.get("chosen_operation")
            calculation_base = request.form.get("result_base")
            print(number1, base1, number2, base2, operation, calculation_base)

            try:
                calculation_result = Converter.get_calculated_number(int(number1), int(base1), int(number2),
                                                                     int(base2), int(calculation_base), operation)
                session["result"] = calculation_result
                session["color"] = Config.Correct_Font_Color
                session["return_page"] = "calculator"
                flash("result_access_granted")
                return redirect(url_for("result"))
            except ValueError:
                flash(program.Text_Base[lang]["convertion_error"], "danger")
                return redirect(url_for("calculator"))

    calculator_checked = "checked"
    return program.get_rendered_template("calculator.html", user, calculator_checked)


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
    train_checked = "checked"
    return program.get_rendered_template("train.html", user, task_text, train_checked)


@app.route("/result", methods=["GET", "POST"])
def result():
    program.init()

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
        case "converter" | "calculator":
            user_result = session.get("result")
        case "train":
            user_result = program.get_task_result(user)
        case _:
            raise Exception("Unknown source page")

    color = session.get("color")
    return_page = session.get("return_page")

    return program.get_rendered_template("result.html", user, user_result, color, return_page)


@app.route("/register", methods=["GET", "POST"])
def register():
    program.init()

    if "user_id" in session:
        return redirect(url_for("logout"))

    lang = session.get("language")

    if request.method == "POST":
        action = request.form.get("action")
        if not program.process_action(action, request, session):
            username = request.form["username"]
            password_1 = request.form["password_1"]
            password_2 = request.form["password_2"]

            if User.query.filter_by(username=username).first():
                flash(program.Text_Base[lang]["existed_username_alert"], "danger")
                return redirect(url_for("register"))

            if password_1 != password_2:
                flash(program.Text_Base[lang]["different_passwords_alert"], "danger")
                return redirect(url_for("register"))

            new_user = User(username=username)
            new_user.set_password(password_1)
            new_user.language = session.get("language")
            new_user.theme = session.get("theme")

            db.session.add(new_user)
            db.session.commit()

            flash(program.Text_Base[lang]["registration_success"], "success")
            return redirect(url_for("login"))

    return program.get_rendered_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    program.init()

    if "user_id" in session:
        return redirect(url_for("logout"))

    if request.method == "POST":
        action = request.form.get("action")
        if not program.process_action(action, request, session):
            username = request.form["username"]
            password = request.form["password"]

            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session["user_id"] = user.id
                return redirect(url_for("train"))
            else:
                lang = session.get("language")
                flash(program.Text_Base[lang]["invalid_login_data"], "danger")

    return program.get_rendered_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)

    lang = session.get("language")
    text = program.Text_Base[lang]

    flash(text["logout_success"], "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()
