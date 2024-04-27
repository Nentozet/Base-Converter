from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

exp = []
LANGUAGE = 'ru'

with open('text.json', encoding='utf8') as text_json:
    TEXT = json.load(text_json)


def convert_base(number, from_base, to_base):
    if from_base == 10:
        number_in_decimal = int(str(number), 10)
    else:
        number_in_decimal = int(str(number), from_base)

    if to_base == 10:
        return str(number_in_decimal)
    else:
        if to_base == 2:
            return bin(number_in_decimal)[2:]
        elif to_base == 3:
            return basechange(number_in_decimal, 3)
        elif to_base == 4:
            return basechange(number_in_decimal, 4)
        elif to_base == 16:
            return hex(number_in_decimal)[2:]


def basechange(number, base):
    result = ''
    while number > 0:
        result = str(number % base) + result
        number = number // base
    return result


@app.route('/', methods=['GET', 'POST'])
def welcome():
    global LANGUAGE
    if request.method == 'GET':
        return render_template('welcome.html', **TEXT[LANGUAGE])
    else:
        LANGUAGE = request.form.get('lang')
        return redirect('/converter')


@app.route('/converter')
def convert():
    return render_template('converter.html', **TEXT[LANGUAGE])


@app.route('/result', methods=['GET', 'POST'])
def converter():
    result = None
    if request.method == 'POST':
        from_notation = request.form['from_notation']
        to_notation = request.form['to_notation']
        number_to_convert = request.form['number_to_convert']

        try:
            result = convert_base(number_to_convert, int(from_notation), int(to_notation))
        except Exception as e:
            exp.append(e)
            result = TEXT[LANGUAGE]["error"]

    return render_template('result.html', result=result, **TEXT[LANGUAGE])


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
