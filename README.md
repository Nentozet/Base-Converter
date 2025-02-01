## ***Введение***
**Base Converter API** позволяет:
+	Конвертировать числа между системами счисления.
+	Выполнять различные арифметические операции (сложение, вычитание, умножение, деление) между числами в различных системах счисления.
+	Генерировать задания для обучения или тестирования пользователей на всех поддерживаемых языках (русский, английский, немецкий, французский, японский).
Для доступа к функциям API авторизация не требуется.

## **Формат запросов и ответов**
Базовый URL: 
>https://base-converter.onrender.com/api/

Все параметры должны передаются по имени, через знак = нужно указать значение. Каждая такая пара ```имя-значение``` отделяется друг от друга знаком ```&```. Сами параметры могут указываться в произвольном порядке.
Главным параметром является ```mode```, который может принимать следующие значения:

1. ```converter``` – режим конвертера.
- Формат ответа:
   - Обязательные аргументы:
      - ```from_number=<любое число>``` - число для преобразования.
      - ```from_base=<натуральное число в диапазоне [2, 36]>``` - основание числа from_number.
      - ```to_base=< натуральное число в диапазоне [2, 36]>``` - основание преобразованного числа.
   - Необязательные аргументы:
      - ```accuracy = <натуральное число в диапазоне [1, 100]>```- натуральное число в диапазоне [2, 36].
- Формат ответа:
     ```
     {
        "status": ...,
        "error_description": ...,
        "result": ...
     }
     ```
     - ```"status"``` - статус запроса. Возможные значения:
        - ```ok``` - сервером был получен *корректный* запрос.
        - ```error``` - сервером был получен *некорректный* запрос.
     - ```"error_description"``` - Описание ошибки, если таковая произошла. Если ```"status": "ok"```, то ```"error_description"``` в json-файле отсутствует. Возможные значения:
        - ```Incorrect parameters specified``` - введеные параметры не соответствуют структуре запроса.
     - ```"result"``` - Результат преобразования числа. Если ```"status": "error"```, то ```"result"``` в json-файле отсутствует.
### **Пример запроса**:
> https://base-converter.onrender.com/api/mode=converter&from_number=5.142423&from_base=10&to_base=2&accuracy=6
 ```json
{
  "result": "101.001001",
  "status": "ok"
}
 ```

  












# ***Важные особенности***
+ Веб-приложение поддерживает ***десятичную***, ***бинарную(двоичную)***, ***шестнадцатеричную***, ***троичною*** и ***четверичную*** системы счисления.
+ Поддержка ***русского***, ***английского***, ***немецкого***, ***французского*** и ***японского*** языков.
+ ***Простой*** и ***лаконичный*** дизайн.
___
# ***Архитектура***
+ Конвертер реализован на базе библеотеки ***flask*** с помощью модулей `Flask`, `render_template`, `request`, `redirect`.
+ Основной файл программы - `converter.py`.
+ Три файла `welcome.html`, `converter.html` и `result.html` содержат пользовательский интерфейс веб-приложения.
+ Файл `text.json` содержит всю информацию о текстовой составляющей(надписях) на разных языках.
