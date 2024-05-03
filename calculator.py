import tkinter as tk
import math


class CombinedCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Combined Calculator")
        self._create_widgets()

    def _create_widgets(self):
        self.display = tk.StringVar()
        entry_display = tk.Entry(self, textvariable=self.display, justify='right', font=('Arial', 20))
        entry_display.grid(row=0, column=0, columnspan=5, sticky='nsew')

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3), ('cos', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3), ('sin', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3), ('tan', 3, 4),
            ('0', 4, 1), ('C', 4, 0), ('=', 4, 2), ('/', 4, 3), ('^', 4, 4),
            ('x!', 5, 0), ('√x', 5, 1), ('сtan', 5, 2), ('(', 5, 3), (')', 5, 4)
        ]

        for (text, row, col) in buttons:
            if text == '=':
                btn = tk.Button(self, text=text, command=self._evaluate_expression, font=('Arial', 18))
            elif text == 'C':
                btn = tk.Button(self, text=text, command=self._clear_display, font=('Arial', 18))
            else:
                btn = tk.Button(self, text=text, command=lambda t=text: self._insert_value(t), font=('Arial', 18))
            btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)

        for i in range(1, 6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

    def _insert_value(self, value):
        current = self.display.get()
        operators = ['+', '-', '*', '/']
        functions = {
            'cos': math.cos,
            'sin': math.sin,
            'tan': math.tan,
            'сtan': lambda x: 1 / math.tan(x),
            'x!': math.factorial,
            '√x': math.sqrt,
        }

        if value in functions and current:
            try:
                if current[-1] in operators or current[-1] in '^()':
                    # Преобразование текущего значения в радианы, если это тригонометрическая функция
                    if value in ['cos', 'sin', 'tan', 'ctan']:
                        radian_value = math.radians(float(current[-2]))
                        result = functions[value](radian_value)
                    elif 'x!' in value:
                        try:
                            num = int(float(current[-2]))  # Преобразуем текущее значение в целое число
                            result = math.factorial(num)
                            self.display.set(str(result))
                        except ValueError:
                            self.display.set("Error")
                        except OverflowError:
                            self.display.set("Too large")
                    else:
                        # Для функций не требующих преобразования в радианы
                        result = functions[value](float(current[-2]))
                    self.display.set(str(result))
                else:
                    # Преобразование текущего значения в радианы, если это тригонометрическая функция
                    if value in ['cos', 'sin', 'tan', 'ctan']:
                        radian_value = math.radians(float(current))
                        result = functions[value](radian_value)
                    elif 'x!' in value:
                        try:
                            num = int(float(current))  # Преобразуем текущее значение в целое число
                            result = math.factorial(num)
                            self.display.set(str(result))
                        except ValueError:
                            self.display.set("Error")
                        except OverflowError:
                            self.display.set("Too large")
                    else:
                        # Для функций не требующих преобразования в радианы
                        result = functions[value](float(current))
                    self.display.set(str(result))
            except Exception as e:
                self.display.set("Error")
        elif value in operators and current:
            if current[-1] in operators:
                # Если последний символ - оператор, заменяем его на новый оператор
                self.display.set(current[:-1] + value)
            elif current[-1] == '^' and value != '-':
                self.display.set("Error")
            else:
                # Добавляем оператор, если последний символ не оператор
                self.display.set(current + value)
        elif value in '()':
            if value == '(':
                if current and (current[-1].isdigit() or current[-1] == ')'):
                    # Добавить умножение, если скобка идет после числа или закрытой скобки
                    self.display.set(current + '*' + value)
                else:
                    self.display.set(current + value)
            elif value == ')':
                if current.count('(') > current.count(')'):
                    # Добавить закрывающую скобку только если есть открывающие без закрывающих
                    self.display.set(current + value)
                    if current[-1] in operators or current[-1] == '^':
                        # Если последний символ - оператор, заменяем его на новый оператор
                        self.display.set(current[:-1] + value)
                    else:
                        # Добавляем оператор, если последний символ не оператор
                        self.display.set(current + value)
        elif value == '^':
            # Разрешить ввод оператора степени только если последний символ является числом или закрывающей скобкой
            if current and (current[-1].isdigit() or current[-1] == ')'):
                self.display.set(current + '^')
            else:
                self.display.set(current)  # Игнорировать некорректный ввод
        else:
            self.display.set(current + value)

    def _evaluate_expression(self):
        try:
            expression = self.display.get()
            expression = expression.replace('^', '**')  # Замена, если пользователь ввел ^
            result = eval(expression)
            self.display.set(str(result))
        except Exception as e:
            self.display.set("Error")
            self.after(2000, self._clear_display) 

    def _clear_display(self):
        self.display.set("")



# The running of the calculator would be done outside in a conditional block:
if __name__ == "__main__":
    app = CombinedCalculator()
    app.mainloop()
