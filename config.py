class Config:
    Default_Language = "ru"
    Default_Theme = "dark"
    Correct_Font_Color = "#00b400"
    Conversion_Accuracy = 12
    Calculation_Accuracy = 12
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

    Task_Arg_Names_Changer = {
        'type': 'task_type',
        'lang': 'lang'
    }
