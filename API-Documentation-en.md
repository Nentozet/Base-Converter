
# **Introduction**<span id="introduction"></span>
**Base Converter API** provides access to the main functions of **Base Converter**, namely:
- Convert numbers between numeral systems.
- Perform various arithmetic operations (addition, subtraction, multiplication, division) between numbers in different numeral systems.
- Generate tasks for training or testing users in all supported languages:
  
    - Russian
    - English
    - German
    - French
    - Japanese

> [!NOTE]
> Authorization is not required to access API functions.
___

# **Request Format**<span id="requests_format"></span>
Base URL: 
>https://base-converter.onrender.com/api/

> [!IMPORTANT]
> All parameters must be passed by name, using the ```=``` sign to specify the value.> Each such "name-value" pair is separated by the ```&``` sign.> Parameters can be specified in any order.

The main parameter is ```mode```, which can take the following values:

## ```mode=converter``` – converter mode.<span id="request_converter"></span>
***Required*** **arguments:**
   - ```fn=<any number>``` - number to be converted.
   - ```fb=<integer in the range [2, 36]>``` - base of the number ```fn```.
   - ```tb=<integer in the range [2, 36]>``` - base of the converted number.

***Optional*** **arguments:**
   - ```accuracy=<integer in the range [1, 100]>``` - maximum number of digits in the fractional part of the number(default ```12```).

## ```mode=calculator``` – calculator mode.<span id="request_calculator"></span>
***Required*** **arguments:**
   - ```n1=<any number>``` - first number.
   - ```b1=<integer in the range [2, 36]>``` - base of the number n1.
   - ```n2=<any number>``` - second number.
   - ```b2=<integer in the range [2, 36]>``` - base of the number n2.
   - ```oper=<operation code>``` - operation type between numbers n1 and n2.

     |       Operation Type        |      Operation Code       |
     | :-------------------------: | :-----------------------: |
     | Addition                    | add                       |
     | Subtraction                 | sub                       |
     | Multiplication              | mult                      |
     | Division                    | div                       |
   - ```calc_b=<integer in the range [2, 36]>``` - base of the result number.

***Optional*** **arguments:**
   - ```accuracy=<integer in the range [1, 100]>``` - maximum number of digits in the fractional part of the number(default ```12```).

## ```mode=task_generator``` – task generator mode.<span id="request_task_generator"></span>
***Required*** **arguments:**
   - ```type=<task type number>``` - task type.

     | Task Type | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Task Statement |
     | :-------: | :----------------------------------------------------------------------------------------------------- |
     | 1 | Convert the number ```<random integer>``` to the numeral system ```<random integer in the range [2, 36]>``` (do not specify the base in the answer). |
     | 2 | How many integers ```x``` satisfy the following double inequality: ```<random integer>``` **<sign </&#8804;>** ```x``` **<sign </&#8804;>** ```<random integer>```? |
     | 3 | Find the value of the expression and write it in the number system  ```<random integer in the range [2, 36]>```: ```<random integer>``` **<sign of operation (+, -, * or /)>** ```<random integer>``` |
   - ```lang=<language code>``` - language to which the task statement will be translated.

     |    Language    | Language Code |
     | :------------: | :-----------: |
     | Russian        | ru            |
     | English        | gb            |
     | German         | de            |
     | French         | fr            |
     | Japanese       | jp            |
___

# **Response Format**<span id="responses_format"></span>
After processing the request, a **JSON file** is returned as a response.

### For [**converter**](#request_converter) and [**calculator**](#request_calculator):
```
{
 "status": ...,
 "error_description": ...,
 "result": ...
}
```
- ```"status"``` - request status. Possible values:
   - ```ok``` - the server successfully processed the request.
   - ```error``` - the server failed to process the request correctly.

- ```"error_description"``` - error description, if any. Possible values:
   - ```Incorrect parameters specified``` - the provided parameters do not match the request structure.
> If ```"status": "ok"```, the ```"error_description"``` attribute is not present in the JSON object.

- ```"result"``` - resulting number.
> If ```"status": "error"```, the ```"result"``` attribute is not present in the JSON object.

### For [**task_generator**](#request_task_generator):
```
{
  "status": ...,
  "error_description": ...,
  "result":
  {
    "text": ...,
    "correct_answer": ...
  }
}
```
- ```"status"``` - request status. Possible values:
   - ```ok``` - the server successfully processed the request.
   - ```error``` - the server failed to process the request correctly.

- ```"error_description"``` - error description, if any. Possible values:
   - ```Incorrect parameters specified``` - the provided parameters do not match the request structure.
> If ```"status": "ok"```, the ```"error_description"``` attribute is not present in the JSON object.

- ```"result"``` - nested object containing two attributes:
   - ```text``` - task statement in the requested language.
   - ```correct_answer``` - correct answer to the task.
> If ```"status": "error"```, the ```"result"``` attribute is not present in the JSON object.
___

# **Examples**<span id="examples"></span>
> Convert the number **5.142423** from the **decimal** numeral system to the **binary** system with a maximum precision of **6 digits** in the fractional part.\
> https://base-converter.onrender.com/api/mode=converter&fn=5.142423&fb=10&tb=2&accuracy=6
```json
{
   "status": "ok",
   "result": "101.001001"
}
```
> Divide the number **40** with base **10** by the number **3** with base **10** and get the result written in the **binary** numeral system with a maximum precision of **3 digits** in the fractional part.\
> https://base-converter.onrender.com/api/mode=calculator&n1=40&b1=10&n2=3&b2=10&calc_b=2&oper=div&accuracy=3
```json
{
  "status": "ok",
  "result": "1101.01"
}
```
> Generate a task of type **1** in **Russian language**.\
> https://base-converter.onrender.com/api/mode=task_generator&type=2&lang=gb
```json
{
  "status": "ok",
  "result":
  {
    "text": "How many integers x satisfy the following double inequality: 31₂₃ < x < 160₂₀?",
    "correct_answer": "449"
  }
}
```

