from flask import session
from toolset import Toolset
from converter import Converter
from config import Config
import random


class Task_Manager:
    __Bases_For_Task = range(2, 37)

    __Left_Border_For_Number = 20
    __Right_Border_For_Number = 1000

    @staticmethod
    def get_random_number_base(preferences=""):
        base = random.choice(Task_Manager.__Bases_For_Task)

        delta = Task_Manager.__Right_Border_For_Number - Task_Manager.__Left_Border_For_Number
        match preferences:
            case "":
                left_border = Task_Manager.__Left_Border_For_Number
                right_border = Task_Manager.__Left_Border_For_Number + delta

            case "first_half":
                left_border = Task_Manager.__Left_Border_For_Number
                right_border = Task_Manager.__Left_Border_For_Number + delta // 2

            case "second_half":
                left_border = Task_Manager.__Left_Border_For_Number + delta // 2
                right_border = Task_Manager.__Left_Border_For_Number + delta

            case _:
                raise Exception("Unknown preference")

        number = Converter.get_converted_number(str(random.randint(left_border, right_border)), 10, base)

        return number, base

    @staticmethod
    def get_text(text_base, task_data, task_type):
        replacements = task_data.split("|")
        return Toolset.replace_underscores(text_base[f"task_{task_type}"], replacements)

    @staticmethod
    def get_result(text_base, correct_answer_format):
        if session.get("last_answer_correct"):
            return text_base["correct"]
        else:
            return text_base["incorrect"].replace("_", correct_answer_format)

    @staticmethod
    def check_answer(answer, correct_answers):
        if answer == correct_answers[0]:
            session["color"] = Config.Correct_Font_Color
            session["last_answer_correct"] = True
            return True
        else:
            session["color"] = "#ff0000"
            session["last_answer_correct"] = False
            return False

    @staticmethod
    def __get_task_1():
        from_number, from_base = Task_Manager.get_random_number_base()

        to_base = random.choice(Task_Manager.__Bases_For_Task)
        while to_base == from_base:
            to_base = random.choice(Task_Manager.__Bases_For_Task)

        to_number = Converter.get_converted_number(from_number, from_base, to_base)

        # Возвращаем данные задания для пользователя
        data = "|".join([Toolset.get_number_with_base(from_number, from_base), str(to_base)])
        correct_answers = "|".join([to_number, Toolset.get_number_with_base(to_number, to_base)])

        return data, correct_answers

    @staticmethod
    def __get_task_2():
        first_comparison_sign, second_comparison_sign = random.choice(["<", "≤"]), random.choice(["<", "≤"])

        number_1, base_1 = Task_Manager.get_random_number_base("first_half")
        number_1_dec = int(str(number_1), base_1)

        number_2, base_2 = Task_Manager.get_random_number_base("second_half")
        number_2_dec = int(str(number_2), base_2)

        while number_1_dec == number_2_dec:
            number_2, base_2 = Task_Manager.get_random_number_base("second_half")
            number_2_dec = int(str(number_2), base_2)

        delta = number_2_dec - number_1_dec

        if first_comparison_sign == second_comparison_sign:
            if first_comparison_sign == "<":
                delta -= 1
            else:
                delta += 1

        # Возвращаем данные задания для пользователя
        correct_answers = str(delta)

        number_1_format = Toolset.get_number_with_base(number_1, base_1)
        number_2_format = Toolset.get_number_with_base(number_2, base_2)

        data = "|".join([number_1_format, first_comparison_sign, second_comparison_sign, number_2_format])

        return data, correct_answers

    @staticmethod
    def __get_task_3():
        operators = Config.Task_3_Operations_Weight.items()
        operators_with_weight = [oper for oper, weight in operators for _ in range(weight)]
        operation = random.choice(operators_with_weight)

        number1, base1 = Task_Manager.get_random_number_base()
        number1_dec = int(str(number1), base1)

        number2, base2 = Task_Manager.get_random_number_base()
        number2_dec = int(str(number2), base2)

        if operation == "/":
            if number1_dec < number2_dec:
                number1, base1, number2, base2 = number2, base2, number1, base1
                number1_dec, number2_dec = number2_dec, number1_dec
            if number1_dec != number1_dec - number1_dec % number2_dec:
                number1_dec -= number1_dec % number2_dec
                number1 = Converter.get_converted_number(number1_dec, 10, base1)

        res_base = random.choice(Task_Manager.__Bases_For_Task)

        res = Converter.get_calculated_number(number1, base1, number2, base2, res_base, operation,
                                              need_base_notation=False)
        correct_answers = "|".join([res, Toolset.get_number_with_base(res, res_base)])

        number1_format = Toolset.get_number_with_base(number1, base1)
        number2_format = Toolset.get_number_with_base(number2, base2)

        data = "|".join([str(res_base), number1_format, operation, number2_format])

        return data, correct_answers

    @staticmethod
    def generate_task(task_type):
        task_type = int(task_type)
        match task_type:
            case 1:
                data, correct_answers = Task_Manager.__get_task_1()
            case 2:
                data, correct_answers = Task_Manager.__get_task_2()
            case 3:
                data, correct_answers = Task_Manager.__get_task_3()
            case _:
                raise Exception(f"{task_type} task doesn't exist")

        return data, correct_answers
