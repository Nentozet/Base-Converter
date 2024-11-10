from flask import session, render_template
from config import Config
from user import db
from task import TaskManager
import inspect
import json


class Program:
    exp = []
    with open("text.json", encoding="utf8") as text_json:
        Text_Base = json.load(text_json)

    def __init__(self):
        self.task_manager = TaskManager()

    @staticmethod
    def init():
        if not session.get("language") or not session.get("theme"):
            session["language"] = Config.Default_Language
            session["theme"] = Config.Default_Theme

    @staticmethod
    def process_action(action, request, user=0):
        match action:
            case None:
                return False

            case "change_language":
                if user:
                    user.language = request.form.get("lang")
                    db.session.commit()

                session["language"] = request.form.get("lang")
                return True

            case "switch_theme_light" | "switch_theme_dark":
                if user:
                    user.theme = action.split("_")[-1]
                    db.session.commit()
                session["theme"] = action.split("_")[-1]
                return True

            case _:
                raise Exception("Program doesn't know about this action")

    def check_answer_for_task(self, answer, user):
        return self.task_manager.check_answer(answer, user)

    def reset_task(self, task_type, user):
        self.task_manager.reset_task(task_type, user)

    def get_task_text(self, user):
        return self.task_manager.get_text(self.Text_Base[user.language], user)

    def get_task_result(self, user):
        return self.task_manager.get_result(self.Text_Base[user.language], user)

    def get_rendered_template(self, filename, user=0, *args):
        # !!! В качестве аргументов этой функции должны передаваться переменные с таким же названием, что и в html-файле
        if user:
            theme = user.theme
            language = user.language
            username_ = user.username
        else:
            theme = session.get("theme")
            language = session.get("language")
            username_ = 0

        data = {
            "base_filename": f"base_{theme}.html",
            "icon": language,
            "username_": username_,
            **self.Text_Base[language]
        }

        for arg in args:
            callers_locals = inspect.currentframe().f_back.f_locals
            arg_name_list = [name for name, value in callers_locals.items() if value is arg]
            if len(arg_name_list) != 0:
                arg_name = arg_name_list[0]
                data[arg_name] = arg

        return render_template(filename, **data)
