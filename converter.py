from toolset import Toolset
from config import Config
from decimal import Decimal, getcontext


class Converter:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @staticmethod
    def get_converted_number(number, from_base, to_base):
        getcontext().prec = Config.Conversion_Precision * 4
        number = Converter.__get_validated_number(number)

        if number[0] == "-":
            negative = "-"
            number = number[1:]
        else:
            negative = ""

        if from_base != 10:
            number_dec = str(Converter.__change_base_to_dec(number, from_base))
        else:
            number_dec = number

        return negative + Converter.__change_base_from_dec(number_dec, to_base)

    @staticmethod
    def get_calculated_number(number1, base1, number2, base2, calculation_base, operation):
        number1 = Converter.get_converted_number(number1, base1, 10)
        number2 = Converter.get_converted_number(number2, base2, 10)

        expression = f' {operation} '.join((number1, number2))
        calculation_result_dec = str(eval(expression))

        if calculation_base != 10:
            calculation_result = Converter.get_converted_number(calculation_result_dec, 10, calculation_base)
        else:
            calculation_result = calculation_result_dec

        if '.' in calculation_result:
            calculation_result = calculation_result.rstrip('0')

        calculation_result_format = Toolset.get_number_with_base(calculation_result, calculation_base)

        return calculation_result_format

    @staticmethod
    def __change_base_to_dec(number, base):
        if '.' in number:
            integer_part, frac_part = number.split('.')
        else:
            integer_part, frac_part = number, ''

        integer_value = 0
        for i, digit in enumerate(reversed(integer_part)):
            integer_value += int(digit, base) * (base ** i)

        fractional_value = Decimal(0)
        if frac_part:
            for i, digit in enumerate(frac_part, start=1):
                fractional_value += Decimal(int(digit, base)) * (Decimal(1.0) / Decimal(base ** i))

        return integer_value + fractional_value

    @staticmethod
    def __change_base_from_dec(number, base):
        if base == 10:
            return number

        if '.' in number:
            integer_part, fractional_part = number.split('.')
        else:
            integer_part, fractional_part = number, ''

        # Преобразование целой части
        integer_part = int(integer_part)
        result_integer = ''
        if integer_part == 0:
            result_integer = '0'
        else:
            while integer_part > 0:
                digit = integer_part % base
                result_integer = Converter.digits[digit] + result_integer
                integer_part //= base

        # Преобразование дробной части
        result_fractional = ''
        if fractional_part:
            fractional_part = Decimal(f'0.{fractional_part}')
            for _ in range(Config.Conversion_Precision):  # Точность до Config.Conversion_Precision знаков
                fractional_part *= base
                digit = int(fractional_part)
                result_fractional += Converter.digits[digit]
                fractional_part -= digit
                if fractional_part == 0:
                    break

        # Объединение результата
        result = result_integer
        if result_fractional:
            result += '.' + result_fractional

        return result

    @staticmethod
    def __get_validated_number(number):
        number = number.replace(" ", "").replace(",", ".").lstrip("0")

        if number == "":
            return 0
        
        if number.count(".") > 1:
            raise ValueError

        if number[0] == "-":
            negative = "-"
            number = number[1:]
        else:
            negative = ""

        if '.' in number:
            int_part, frac_part = number.split('.')
            if int_part == '':
                int_part = '0'
            frac_part = frac_part.rstrip('0')
        else:
            int_part, frac_part = number, ''

        if frac_part == '':
            return negative + int_part
        else:
            return negative + int_part + '.' + frac_part
