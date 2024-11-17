from toolset import Toolset


class Converter:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @staticmethod
    def get_converted_number(number, from_base, to_base):
        number_in_decimal = int(str(number), from_base)

        return Converter.__change_base_from_dec(number_in_decimal, to_base)

    @staticmethod
    def get_calculated_number(number1, base1, number2, base2, calculation_base, operation):
        number1 = Converter.get_converted_number(number1, base1, 10)
        number2 = Converter.get_converted_number(number2, base2, 10)

        expression = f' {operation} '.join((number1, number2))
        calculation_result_dec = round(eval(expression), 4)

        calculation_result = Converter.get_converted_number(calculation_result_dec, 10, calculation_base)

        calculation_result_format = Toolset.get_number_with_base(calculation_result, calculation_base)

        return calculation_result_format

    @staticmethod
    def __change_base_from_dec(number, base):
        if number < base:
            return Converter.digits[number]
        else:
            return Converter.__change_base_from_dec(number // base, base) + Converter.digits[number % base]
