class Converter:
    @staticmethod
    def get_converted_number(number, from_base, to_base):
        number_in_decimal = int(str(number), from_base)

        return Converter.__change_base_from_dec(number_in_decimal, to_base)

    @staticmethod
    def __change_base_from_dec(number, base):
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if number < base:
            return digits[number]
        else:
            return Converter.__change_base_from_dec(number // base, base) + digits[number % base]
