from string import ascii_letters, digits


class Config:
    Default_Language = "ru"
    Default_Theme = "dark"
    Correct_Font_Color = "#00b400"
    Conversion_Accuracy = 12
    Calculation_Accuracy = 12

    Username_Min_Symbols_Count = 4
    Username_Max_Symbols_Count = 20
    User_Password_Min_Symbols_Count = 5
    User_Password_Max_Symbols_Count = 25

    Converter_Arg_Names_Changer = {
        'fn': 'from_number',
        'fb': 'from_base',
        'tb': 'to_base',
        'accuracy': 'accuracy'
    }
    Calculator_Arg_Names_Changer = {
        'n1': 'number1',
        'b1': 'base1',
        'n2': 'number2',
        'b2': 'base2',
        'oper': 'operation',
        'calc_b': 'calculation_base',
        'accuracy': 'accuracy'
    }
    Operation_Args_Changer = {
        'add': '+',
        'sub': '-',
        'mult': '*',
        'div': '/',
    }

    Task_3_Operations_Weight = {
        '+': 5,
        '-': 5,
        '*': 5,
        '/': 2
    }

    Task_Arg_Names_Changer = {
        'type': 'task_type',
        'lang': 'lang'
    }

    Cyrillic_Uppercase = ''.join(map(chr, range(ord('А'), ord('Я') + 1)))
    Cyrillic_Lowercase = ''.join(map(chr, range(ord('а'), ord('я') + 1)))

    Available_Symbols = ascii_letters + digits + Cyrillic_Uppercase + Cyrillic_Lowercase
