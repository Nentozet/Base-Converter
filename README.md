# **Введение**<span id="introduction"></span>
**Base Converter API** предоставляет возможность пользоваться главными функциями **Base Converter**, а именно:
+	Конвертировать числа между системами счисления.
+	Выполненять различные арифметические операции (сложение, вычитание, умножение, деление) между числами в различных системах счисления.
+	Генерировать задания для обучения или тестирования пользователей на всех поддерживаемых языках (русский, английский, немецкий, французский, японский).
Для доступа к функциям API авторизация не требуется.
___


# **Формат запроса**<span id="requests_format"></span>
Базовый URL: 
>https://base-converter.onrender.com/api/

> [!IMPORTANT]
> Все параметры должны передаваться по имени, через знак ```=``` нужно указать значение. Каждая такая пара ```имя-значение``` отделяется друг от друга знаком ```&```. Сами параметры могут указываться в произвольном порядке.
Главным параметром является ```mode```, который может принимать следующие значения:
## ```mode=converter``` – режим конвертера.<span id="request_converter"></span>
***Обязательные*** **аргументы:**
   - ```fn=<любое число>``` - число для преобразования.
   - ```fb=<целое число в диапазоне [2, 36]>``` - основание числа ```fn```.
   - ```tb=<целое число в диапазоне [2, 36]>``` - основание преобразованного числа.

***Необязательные*** **аргументы:**
   - ```accuracy=<целое число в диапазоне [1, 100]>```- максимальное количество знаков в дробной части числа.

## ```mode=calculator``` – режим калькулятора.<span id="request_calculator"></span>
***Обязательные*** **аргументы:**
   - ```n1=<любое число>``` - первое число.
   - ```b1=<целое число в диапазоне [2, 36]>``` - основание числа n1.
   - ```n2=<любое число>``` - второе число.
   - ```b2=<целое число в диапазоне [2, 36]>``` - основание числа n2.
   - ```oper=<add/sub/mult/div>``` - тип операции между числами n1 и n2.
   - ```calc_b=<целое число в диапазоне [2, 36]>``` - основание посчитанного числа.

***Необязательные*** **аргументы:**
   - ```accuracy=<целое число в диапазоне [1, 100]>```- максимальное количество знаков в дробной части числа.

## ```mode=task_generator``` – режим генератора задач.<span id="request_task_generator"></span>
***Обязательные*** **аргументы:**
   - ```type=<номер типа задания>``` - тип задания.

     | Тип задачи | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Схема условия |
     | :--------: | :------------ |
     | 1 | Переведите число ```<случайное целое число>``` в систему счисления ```<случайное целое число в диапазоне [2, 36]>``` (основание в ответе указывать не нужно) |
     | 2 | Сколько целых чисел ```x``` удовлетворяет этому двойному неравенству: ```<случайное целое число>``` **<знак </&#8804;>** ```x``` **<знак </&#8804;>** ```<случайное целое число>```? |
   - ```lang=<код языка>``` - язык, на который будет переведено условие.

     | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Язык&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Код языка&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |
     | :--: | :----------: |
     | Русский | ru |
     | Английский | gb |
     | Немецкий | de |
     | Французский | fr |
     | Японский | jp |
___


# **Формат ответа**<span id="responses_format"></span>
После обработки запроса в качестве ответа возвращается **JSON-файл**
### Для [**converter**](#request_converter) и [**calculator**](#request_calculator):
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

- ```"error_description"``` - Описание ошибки, если таковая произошла. Возможные значения:
  - ```Incorrect parameters specified``` - введеные параметры не соответствуют структуре запроса.
> Если ```"status": "ok"```, то ключ ```"error_description"``` в объекте JSON-файла отсутствует.

- ```"result"``` - результирующее число.
> Если ```"status": "error"```, то ключ ```"result"``` в объекте JSON-файла отсутствует.
### Для [**task_generator**](#request_task_generator):
```
{
  "status": ...
  "error_description": ...,
  "result":
  {
    "text": ...,
    "correct_answer": ...
  }
}
```
   - ```"status"``` - статус запроса. Возможные значения:
       - ```ok``` - сервер корректно обработал запрос.
       - ```error``` - у сервера не получилось корректно обработать запрос.
   
   - ```"error_description"``` - Описание ошибки, если таковая произошла. Возможные значения:
      - ```Incorrect parameters specified``` - введеные параметры не соответствуют структуре запроса.
   > Если ```"status": "ok"```, то ключ ```"error_description"``` в объекте JSON-файла отсутствует.
      
   - ```"result"``` - вложенный объект. Содержит два атрибута:
      - ```text``` - условие задачи на указанном в запросе языке.     
      - ```correct_answer``` - правльный ответ на задачу.
   > Если ```"status": "error"```, то ключ ```"result"``` в объекте JSON-файла отсутствует.
___
# **Примеры**:
> Преобразовать число **5.142423** из **десятичной** системы счисления в **двоичную** с максимальной точностью в **6 знаков** в дробной части.\
> https://base-converter.onrender.com/api/mode=converter&from_number=5.142423&from_base=10&to_base=2&accuracy=6
```json
{
   "status": "ok",
   "result": "101.001001"
}
```
> Поделить число **40** с основанием **10** на число **3** с основанием **10** и получить результат, записанный в **двоичной** системе счисления с максимальной точность в **3 знака** в дробной части.\
> https://base-converter.onrender.com/api/mode=calculator&n1=40&b1=10&n2=3&b2=10&calc_b=2&oper=div&accuracy=3
```json
{
  "status": "ok",
  "result": "1101.01"
}
```
> Сгенерировать задачу типа **1** на **русском языке**.\
> https://base-converter.onrender.com/api/mode=task_generator&type=2&lang=ru
```
{
  "status": "ok"
  "result": {
    "correct_answer": "449",
    "text": "Сколько целых чисел x удовлетворяет этому двойному неравенству: 31₂₃ < x < 160₂₀?"
  }
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
