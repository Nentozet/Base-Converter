from flask import render_template, flash
from config import Config
from user import UserManager, db
from task import Task_Manager
import inspect
import json


class Program:
    exp = []
    with open("text.json", encoding="utf8") as text_json:
        Text_Base = json.load(text_json)

    def __init__(self):
        self.task_manager = Task_Manager()
        self.user_manager = UserManager()

    @staticmethod
    def init(ses):
        if not ses.get("language") or not ses.get("theme"):
            ses["language"] = Config.Default_Language
            ses["theme"] = Config.Default_Theme

    def get_user(self, user_id):
        return self.user_manager.get_user(user_id)

    def create_user(self, username, password, ses):
        self.user_manager.create_user(username, password, ses)

    def check_registration_data(self, lang, username, password_1, password_2):
        user = self.user_manager.get_user_by_name(username)
        if user:
            flash(self.Text_Base[lang]["existed_username_alert"], "danger")
            return False

        if not Config.Username_Min_Symbols_Count <= len(username) <= Config.Username_Max_Symbols_Count or \
                not all(symbol in Config.Available_Symbols for symbol in username):
            flash(self.Text_Base[lang]["invalid_username"], "danger")
            return False

        if not Config.User_Password_Min_Symbols_Count <= len(password_1) <= Config.User_Password_Max_Symbols_Count \
                or not all(symbol in Config.Available_Symbols for symbol in password_1):
            flash(self.Text_Base[lang]["invalid_password"], "danger")
            return False

        if password_1 != password_2:
            flash(self.Text_Base[lang]["different_passwords_alert"], "danger")
            return False

        return True

    def check_login_data(self, ses, username, password):
        user = self.user_manager.get_user_by_name(username)
        if user and user.check_password(password):
            ses["user_id"] = user.id
            ses["language"] = user.language
            ses["theme"] = user.theme
            return True

        return False

    @staticmethod
    def process_action(action, request, ses, user=0):
        match action:
            case None:
                return False

            case "change_language":
                if user:
                    user.language = request.form.get("lang")
                    db.session.commit()

                ses["language"] = request.form.get("lang")
                return True

            case "switch_theme_light" | "switch_theme_dark":
                if user:
                    user.theme = action.split("_")[-1]
                    db.session.commit()
                ses["theme"] = action.split("_")[-1]
                return True

            case _:
                raise Exception("Program doesn't know about this action")

    def check_answer_for_task(self, answer, user):
        return self.task_manager.check_answer(answer, user.task_correct_answers.split('|'))

    def reset_task(self, task_type, user):
        if user.need_to_reset_task:
            user.set_task(task_type, *self.task_manager.generate_task(task_type))
            user.need_to_reset_task = False
            db.session.commit()

    def get_task_text(self, language, task_data, task_type):
        return self.task_manager.get_text(self.Text_Base[language], task_data, task_type)

    def get_task_result(self, user):
        return self.task_manager.get_result(self.Text_Base[user.language], user.task_correct_answers.split("|")[-1])

    def get_rendered_template(self, filename, ses, user=0, *args):
        # !!! В качестве *args этой функции должны передаваться переменные с таким же названием, что и в html-файле
        if user:
            theme = user.theme
            language = user.language
            username_ = user.username
            skill, skill_color = user.get_skill_data()
        else:
            theme = ses.get("theme")
            language = ses.get("language")
            username_ = ""
            skill = ""
            skill_color = ""

        data = {
            "base_filename": f"base_{theme}.html",
            "icon": language,
            "username_": username_,
            "skill": self.Text_Base[language].get(skill),
            "skill_color": skill_color,
            **self.Text_Base[language]
        }

        for arg in args:
            callers_locals = inspect.currentframe().f_back.f_locals
            arg_name_list = [name for name, value in callers_locals.items() if value is arg]
            if len(arg_name_list) != 0:
                arg_name = arg_name_list[0]
                data[arg_name] = arg

        return render_template(filename, **data)

    def on_solved_task(self, answer, user):
        user.need_to_reset_task = True
        db.session.commit()

        res = self.check_answer_for_task(answer, user)
        user.calculate_skill_score(res)

    def generate_task(self, lang, task_type):
        data, corr_ans = self.task_manager.generate_task(task_type)
        text = self.task_manager.get_text(self.Text_Base[lang], data, task_type)
        return text, corr_ans
