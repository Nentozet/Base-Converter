import requests
import threading


class Toolset:
    @staticmethod
    def replace_underscores(template, replacements):
        for replacement in replacements:
            template = template.replace("_", replacement, 1)
        return template

    @staticmethod
    def get_number_with_base(number, base):
        base_table = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return str(number) + str(base).translate(base_table)

    @staticmethod
    def keep_alive():
        try:
            requests.get("https://base-converter.onrender.com")
        except Exception as e:
            print(f"Ошибка keep-alive: {e}")
        threading.Timer(10, Toolset.keep_alive).start()
