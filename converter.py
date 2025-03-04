from toolset import Toolset
from config import Config
from decimal import Decimal, getcontext


class Converter:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @staticmethod
    def get_converted_number(from_number, from_base, to_base, accuracy=Config.Conversion_Accuracy):
        accuracy = int(accuracy)
        from_base = int(from_base)
        to_base = int(to_base)
        getcontext().prec = accuracy * 4
        from_number = Converter.__get_validated_number(from_number)

        if not 2 <= from_base <= 36 or not 2 <= to_base <= 36:
            raise ValueError

        if from_number[0] == "-":
            negative = "-"
            from_number = from_number[1:]
        else:
            negative = ""

        if from_base != 10:
            number_dec = str(Converter.__change_base_to_dec(from_number, from_base))
        else:
            number_dec = from_number

        abs_number = Converter.__change_base_from_dec(number_dec, to_base, accuracy)
        if '.' in abs_number:
            abs_number = abs_number.rstrip('0').rstrip('.')

        return negative + abs_number

    @staticmethod
    def get_calculated_number(number1, base1, number2, base2, calculation_base, operation,
                              accuracy=Config.Calculation_Accuracy, need_base_notation=True):
        accuracy = int(accuracy)
        getcontext().prec = accuracy * 4
        if not 1 <= accuracy <= 100:
            raise ValueError
        base1 = int(base1)
        base2 = int(base2)
        calculation_base = int(calculation_base)
        number1 = Converter.get_converted_number(number1, base1, 10)
        number2 = Converter.get_converted_number(number2, base2, 10)

        expression = f' {operation} '.join((f"Decimal('{number1}')", f"Decimal('{number2}')"))
        calculation_result_dec = str(eval(expression))

        if calculation_base != 10:
            calculation_result = Converter.get_converted_number(calculation_result_dec, 10, calculation_base, accuracy)
        else:
            calculation_result = calculation_result_dec

        if '.' in calculation_result:
            calculation_result = calculation_result[:calculation_result.index('.') + accuracy + 1].rstrip('0')

        if calculation_result[-1] == '.':
            calculation_result = calculation_result[:-1]

        if need_base_notation:
            calculation_result = Toolset.get_number_with_base(calculation_result, calculation_base)

        return calculation_result

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
    def __change_base_from_dec(number, base, accuracy):
        # Точность до accuracy знаков
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
            for _ in range(accuracy):
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
        number = str(number).replace(" ", "").replace(",", ".").lstrip("0")

        if number == "":
            return '0'

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

    # @staticmethod
    # def round_for_base(number, base, accuracy):
    #     if '.' not in number:
    #         return number
    #
    #     if accuracy >= len(number) - number.index('.') - 1:
    #         return number
    #
    #     pre_fraq_part = number[number.index('.') - 1] + number[number.index('.') + 1:]
    #
    #     if pre_fraq_part[accuracy + 1] in Converter.digits[base // 2:]:
    #         pre_fraq_part = pre_fraq_part[:accuracy] + Converter.digits[pre_fraq_part[accuracy] % base]
    #     else:
    #         pre_fraq_part = pre_fraq_part[:accuracy + 1]
    #
    #     return (number[:number.index('.') - 1] + pre_fraq_part[0] + '.' + pre_fraq_part[1:]).rstrip('.')
