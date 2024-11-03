from flask import render_template
from user import db
from task import Task
import inspect
import json


class Program:
    exp = []
    with open("text.json", encoding="utf8") as text_json:
        Text_Base = json.load(text_json)

    def __init__(self, language, theme):
        self.task = Task()
        self.language = language
        self.theme = theme

    def process_action(self, action, request, ses, user=0):
        match action:
            case None:
                return False

            case "change_language":
                if user:
                    user.language = request.form.get("lang")
                    db.session.commit()

                self.language = request.form.get("lang")

                return_page = ses.get("return_page")
                if return_page == "train":
                    if user:
                        lang = user.language
                    else:
                        lang = self.language
                    self.task.translate_text(self.Text_Base[lang])
                    self.task.translate_answer(self.Text_Base[lang], ses)
                return True

            case "switch_theme_light" | "switch_theme_dark":
                if user:
                    user.theme = action.split("_")[-1]
                    db.session.commit()
                self.theme = action.split("_")[-1]
                return True

            case _:
                raise Exception("Program doesn't know about this action")

    def check_answer_for_task(self, answer, ses, lang):
        return self.task.check_answer(answer, self.Text_Base[lang], ses)

    def reset_task(self, task_type, lang):
        self.task.reset(task_type, self.Text_Base[lang])

    def get_rendered_template(self, filename, user, *args):
        # !!! В качестве аргументов этой функции должны передаваться переменные с таким же названием, что и в html-файле

        if user:
            theme = user.theme
            language = user.language
        else:
            theme = self.theme
            language = self.language

        data = {
            "base_filename": f"base_{theme}.html",
            "icon": language,
            **self.Text_Base[language]
        }

        for arg in args:
            callers_locals = inspect.currentframe().f_back.f_locals
            arg_name_list = [name for name, value in callers_locals.items() if value is arg]
            if len(arg_name_list) != 0:
                arg_name = arg_name_list[0]
                data[arg_name] = arg

        return render_template(filename, **data)
