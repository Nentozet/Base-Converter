from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint

db = SQLAlchemy()


class User(db.Model):
    __Min_Adaptive_Difficulty_Score = 0
    __Max_Adaptive_Difficulty_Score = 10

    __Max_Correct_Tasks_In_A_Row_Count = 4
    __Min_Correct_Tasks_In_A_Row_Count = 2
    __Max_Incorrect_Tasks_In_A_Row_Count = 3
    __Min_Incorrect_Tasks_In_A_Row_Count = 1

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    language = db.Column(db.String(2))
    theme = db.Column(db.String(20))
    __password_hash = db.Column(db.String(128), nullable=False)
    __skill_level = db.Column(db.Integer, default=0)
    __correct_tasks_in_a_row_count = db.Column(db.Integer, default=0)
    __incorrect_tasks_in_a_row_count = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.__password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.__password_hash, password)

    def on_solved_task(self, is_correctly):
        min_score = self.__Min_Skill_Level
        max_score = self.__Max_Skill_Level

        if is_correctly:
            self.__correct_tasks_in_a_row_count += 1
            self.__incorrect_tasks_in_a_row_count = 0
            tasks_in_a_row = self.__correct_tasks_in_a_row_count
            min_tasks_in_a_row = self.__Min_Correct_Tasks_In_A_Row_Count
            max_tasks_in_a_row = self.__Max_Correct_Tasks_In_A_Row_Count
            dif_delta = 1

        else:
            self.__incorrect_tasks_in_a_row_count += 1
            self.__correct_tasks_in_a_row_count = 0
            tasks_in_a_row = self.__incorrect_tasks_in_a_row_count
            min_tasks_in_a_row = self.__Min_Incorrect_Tasks_In_A_Row_Count
            max_tasks_in_a_row = self.__Max_Incorrect_Tasks_In_A_Row_Count
            dif_delta = -1

        # Проверка превышения одинаково правильно или неправильно решенных подряд задач
        if tasks_in_a_row >= min_tasks_in_a_row:
            # Высчитываем коэфициэнт для получения шанса изменения показателя адаптивной сложности
            ratio = (1.0 - float(max_tasks_in_a_row - tasks_in_a_row) / 3.0)
            if randint(0, 100) <= int(ratio * 100.0):
                self.__skill_level = min(max(self.__adaptive_difficulty_score + dif_delta, min_score), max_score)

                # Сбрасываем счетчик решенных подряд задач в зависимости от того,
                # правильно или неправильно они были решены
                if is_correctly:
                    self.__correct_tasks_in_a_row_count = 0
                else:
                    self.__incorrect_tasks_in_a_row_count = 0

        # self.__solved_tasks_count += 1
        db.session.commit()

    def get_adaptive_difficulty_ratio(self):
        return float(self.__skill_level) / 10.0
