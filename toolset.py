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
