from flask import session
from user import db
from toolset import Toolset
from converter import Converter
from config import Config
import random


class TaskManager:
    __Bases_For_Task = range(2, 37)

    __Left_Border_For_Number = 20
    __Right_Border_For_Number = 1000

    @staticmethod
    def get_random_number_base(preferences=""):
        base = random.choice(TaskManager.__Bases_For_Task)

        delta = TaskManager.__Right_Border_For_Number - TaskManager.__Left_Border_For_Number
        match preferences:
            case "":
                left_border = TaskManager.__Left_Border_For_Number
                right_border = TaskManager.__Left_Border_For_Number + delta

            case "first_half":
                left_border = TaskManager.__Left_Border_For_Number
                right_border = TaskManager.__Left_Border_For_Number + delta // 2

            case "second_half":
                left_border = TaskManager.__Left_Border_For_Number + delta // 2
                right_border = TaskManager.__Left_Border_For_Number + delta

            case _:
                raise Exception("Unknown preference")

        number = Converter.get_converted_number(str(random.randint(left_border, right_border)), 10, base)

        return number, base

    @staticmethod
    def get_text(text_base, user):
        replacements = user.task_data.split("|")
        return Toolset.replace_underscores(text_base[f"task_{user.task_type}"], replacements)

    @staticmethod
    def get_result(text_base, user):
        if session.get("last_answer_correct"):
            return text_base["correct"]
        else:
            return text_base["incorrect"].replace("_", user.task_correct_answers.split("|")[-1])

    @staticmethod
    def reset_task(task_type, user):
        match task_type:
            case 1:
                TaskManager.__reset_task_1(user)
            case 2:
                TaskManager.__reset_task_2(user)
            case _:
                raise Exception(f"{task_type} task doesn't exist")

        user.task_type = task_type
        db.session.commit()

    @staticmethod
    def check_answer(answer, user):
        correct_answers = user.task_correct_answers.split('|')
        if answer == correct_answers[0]:
            session["color"] = Config.Correct_Font_Color
            session["last_answer_correct"] = True
            return True
        else:
            session["color"] = "#ff0000"
            session["last_answer_correct"] = False
            return False

    @staticmethod
    def __reset_task_1(user):
        from_number, from_base = TaskManager.get_random_number_base()

        to_base = random.choice(TaskManager.__Bases_For_Task)
        while to_base == from_base:
            to_base = random.choice(TaskManager.__Bases_For_Task)

        to_number = Converter.get_converted_number(from_number, from_base, to_base)

        # Сохраняем данные задания для пользователя
        user.task_data = "|".join([Toolset.get_number_with_base(from_number, from_base), str(to_base)])
        user.task_correct_answers = "|".join([str(to_number), Toolset.get_number_with_base(to_number, to_base)])

    @staticmethod
    def __reset_task_2(user):
        first_comparison_sign, second_comparison_sign = random.choice(["<", "≤"]), random.choice(["<", "≤"])

        number_1, base_1 = TaskManager.get_random_number_base("first_half")
        number_1_dec = int(str(number_1), base_1)

        number_2, base_2 = TaskManager.get_random_number_base("second_half")
        number_2_dec = int(str(number_2), base_2)

        while number_1_dec == number_2_dec:
            number_2, base_2 = TaskManager.get_random_number_base("second_half")
            number_2_dec = int(str(number_2), base_2)

        delta = number_2_dec - number_1_dec

        if first_comparison_sign == second_comparison_sign:
            if first_comparison_sign == "<":
                delta -= 1
            else:
                delta += 1

        user.task_correct_answers = "|".join([str(delta), str(delta)])

        number_1_format = Toolset.get_number_with_base(number_1, base_1)
        number_2_format = Toolset.get_number_with_base(number_2, base_2)
        user.task_data = "|".join([number_1_format, first_comparison_sign, second_comparison_sign, number_2_format])
