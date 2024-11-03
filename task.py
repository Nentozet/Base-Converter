import random
from toolset import Toolset
from converter import Converter


class Task:
    __Bases_For_Task = range(2, 37)
    # __Min_Right_Border_For_Base = __Bases_For_Task.index(16)
    # __Max_Right_Border_For_Base = __Bases_For_Task.index(36)
    #
    # __Min_Left_Border_For_Number = 10
    # __Max_Left_Border_For_Number = 35
    # __Min_Right_Border_For_Number = 975
    # __Max_Right_Border_For_Number = 1000

    __Left_Border_For_Number = 20
    __Right_Border_For_Number = 1000

    def __init__(self):
        self.text = ""
        self.__type = 1
        self.__data = []
        self.__correct_answer = ""
        self.__format_correct_answer = ""
        self.__last_answer_was_correct = True

    @staticmethod
    def get_random_number_base(preferences=""):
        base = random.choice(Task.__Bases_For_Task)

        delta = Task.__Right_Border_For_Number - Task.__Left_Border_For_Number
        match preferences:
            case "":
                left_border = Task.__Left_Border_For_Number
                right_border = Task.__Left_Border_For_Number + delta

            case "first_half":
                left_border = Task.__Left_Border_For_Number
                right_border = Task.__Left_Border_For_Number + delta // 2

            case "second_half":
                left_border = Task.__Left_Border_For_Number + delta // 2
                right_border = Task.__Left_Border_For_Number + delta

            case _:
                raise Exception("Unknown preference")

        number = Converter.get_converted_number(random.randint(left_border, right_border), 10, base)

        return number, base

    def translate_text(self, text_base):
        self.text = Toolset.replace_underscores(text_base[f"task_{self.__type}"], self.__data)

        # if carry_to_next_line:
        #     task_text = text_base[f"task_{self.__type}"].split("\n")[0]
        #     replace_text = text_base[f"task_{self.__type}"].split("\n")[-1]
        #     self.text = [task_text, Toolset.replace_underscores(replace_text, self.__data)]
        # else:
        #     replace_text = text_base[f"task_{self.__type}"]
        #     self.text = [Toolset.replace_underscores(replace_text, self.__data)]

    def translate_answer(self, text_base, ses):
        if self.__last_answer_was_correct:
            ses["user_result"] = text_base["correct"]
        else:
            ses["user_result"] = text_base["incorrect"].replace("_", self.__format_correct_answer)

    def reset(self, task_type, text_base):
        match task_type:
            case 1:
                self.__reset_task_1()
            case 2:
                self.__reset_task_2()
            case _:
                raise Exception(f"{self.__type} task doesn't exist")

        print(self.__correct_answer)

        self.__type = task_type
        self.translate_text(text_base)

    def get_correct_answer(self):
        return self.__correct_answer

    def check_answer(self, answer, text_base, ses):
        if answer == self.__correct_answer:
            ses["user_result"] = text_base["correct"]
            ses["color"] = "#00b400"
            self.__last_answer_was_correct = True
            return True
        else:
            ses["user_result"] = text_base["incorrect"].replace("_", self.__format_correct_answer)
            ses["color"] = "#ff0000"
            self.__last_answer_was_correct = False
            return False

    def __reset_task_1(self):
        from_number, from_base = Task.get_random_number_base()

        to_base = random.choice(Task.__Bases_For_Task)
        while to_base == from_base:
            to_base = random.choice(Task.__Bases_For_Task)

        to_number = Converter.get_converted_number(from_number, from_base, to_base)

        # Сохраняем данные для задания
        self.__data = [Toolset.get_number_with_base(from_number, from_base), str(to_base)]
        self.__correct_answer = str(to_number)
        self.__format_correct_answer = Toolset.get_number_with_base(to_number, to_base)

    def __reset_task_2(self):
        first_comparison_sign, second_comparison_sign = random.choice(["<", "<="]), random.choice(["<", "<="])

        number_1, base_1 = Task.get_random_number_base("first_half")
        number_1_dec = int(str(number_1), base_1)

        number_2, base_2 = Task.get_random_number_base("second_half")
        number_2_dec = int(str(number_2), base_2)


        while number_1_dec == number_2_dec:
            number_2, base_2 = Task.get_random_number_base("second_half")
            number_2_dec = int(str(number_2), base_2)

        delta = number_2_dec - number_1_dec

        if first_comparison_sign == second_comparison_sign:
            if first_comparison_sign == "<":
                delta -= 1
            else:
                delta += 1

        self.__correct_answer = str(delta)
        self.__format_correct_answer = str(delta)

        format_number_1 = Toolset.get_number_with_base(number_1, base_1)
        format_number_2 = Toolset.get_number_with_base(number_2, base_2)

        self.__data = [format_number_1, first_comparison_sign, second_comparison_sign, format_number_2]
        # print(self.__data)
