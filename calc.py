from math import sin,cos,radians
import string

class String():
    def __init__(self,expression,global_expression):
        self.expression = expression
        self.global_expression = global_expression
        self.commands = {'=':'=','C':'C','clear':'clear','Q':'Q'}
        self.operators = {'+':(1, lambda x,y: x + y, 2),
                          '-':(1, lambda x,y: x - y, 2),
                          '~':(2,lambda x: x * -1,1), # унарный минус
                          '!':(2,lambda x: x, 1),     # унарный плюс
                          '*':(3, lambda x,y: x * y, 2),
                          '/':(3, lambda x,y: x / y, 2),
                          '%':(3, lambda x,y: x % y, 2),
                          '^':(4, lambda x,y: x ** y, 2),
                          'sin':(5, lambda x: sin(radians(x)), 1),
                          'cos':(5, lambda x: cos(radians(x)), 1),
                          '(':(0, None,0)}
        self.error = False
        self.error_message = ''
        self.results = 0
        
    def check_string(self):
        '''
        Убирает пробелы, узнает что прдано на вход: выражение\комманда
        '''
        self.expression = self.expression.replace(' ','')
        if self.expression in self.commands.keys(): # если поступила комманда
            return self.expression, 'Command'
        else:
            return self.expression, 'Expression'    # если выражение 
        
    def errors(self,n_error,val=None,i=None):
        if n_error == 1: 
            self.error_message = "Выражение не может иметь символ '{}'. Позиция: {}".format(val,i)
            self.error = True
        elif n_error == 2: 
            self.error_message = "Выражение может начинаться с '+','-' или числа. Позиция: {}".format(i)
            self.error = True   
        elif n_error == 3:
            self.error_message = "Выражение не может быть вычислено"
            self.error = True   
        elif n_error == 4:
            self.error_message = "Выражение не может быть дополнено, нет связующего знака"
            self.error = True
        elif n_error == 5: 
            self.error_message = ""
            self.error = True     

    def __str__(self):
        print(self.expression)

class Command(String):
    def __init__(self,expression,global_expression):
        super().__init__(expression,global_expression)

    def execute_command(self):
        if self.expression == self.commands['C']: # сброс последнего выражения
            try:
                self.global_expression.pop()
            except:
                return 'NtR'
        elif self.expression == self.commands['clear']:
            while len(self.global_expression) != 0:
                self.global_expression.pop()
            return 'NtR'
        elif self.expression == self.commands['=']:
            return False
        elif self.expression == self.commands['Q']:
            return True  

class Expression(String):    
    def __init__(self,expression,global_expression):
        super().__init__(expression,global_expression)

    def check_put_string(self):
        '''
        Проверяет выражение и кладет его в глобальную строку
        '''
        prefix_operators_available = {'+':1, '-':1,'sin(':1,'cos(':1, '^':0, '/':0, '%':0, '*':0}

        def check_brackets(expression):
            '''
            Если подается только "(" или ")", то ошибка
            Если кол-во скобок не равно, то ошибка
            Если выражение только из скобок
                Если перед "(" число, то возбужденое ошибки
                Если после "(" ")" , то возбужденое ошибки
                Если после ")" "(" , то возбужденое ошибки
            '''
            if expression == '(' or expression == ')':
                raise Exception()
            elif expression.count('(') != expression.count(')'):
                raise Exception()
            elif len(expression) == expression.count('(') + expression.count(')'):
                raise Exception()
            for i,let in enumerate(expression):
                try:
                    prev = int(expression[i-1])
                except:
                    prev = ''
                try:
                    exp = expression[i+1]
                except:
                    exp = expression[-1]
                if let == '(' and type(prev) == type(0) and prev >= 0:
                    raise Exception()
                elif let == '(' and exp == ')':
                    raise Exception()
                elif let == ')' and exp == '(':
                    raise Exception()
        
        def check_repetitive_operations(expression):
            '''
            Две операции подряд не допускаются "-+", "*%", ...
            '''
            error = 0
            for k, key in enumerate(prefix_operators_available.keys()):
                pos = 0
                if error == 0:
                    string = expression
                    while pos != -1:
                        pos = string.find(key)
                        if pos == -1:
                            break
                        try:
                            next_elem = pos + 1
                            if string[next_elem] in prefix_operators_available.keys() and key == string[next_elem]:                            
                                pos,error = -1, 1
                            else:
                                string = string[pos+1:]
                        except:
                            pos = -1
                else:
                    raise Exception()

        def check2ways(expression,global_expression):
                if len(global_expression) == 0:
                    try:
                        int(expression[0])
                        compile(expression,'<string>','exec')
                        global_expression.append(expression)
                    except:
                        for p in prefix_operators_available.keys(): 
                            if prefix_operators_available[p] == 1: # только оператоы + - в начале
                                if expression.find(p) == 0 and len(expression) == len(p): # если выражение содержит только + или -
                                    global_expression.append(expression)
                                    break
                                elif expression.find(p) == 0: #!    # если выражение содержит sin,cos,+,- в начале
                                    try:
                                        compile(expression,'<string>','exec')
                                        global_expression.append(expression)
                                        break
                                    except:
                                        raise Exception()
                                elif expression[0] == '(':
                                    try:
                                        compile(expression,'<string>','exec')
                                        global_expression.append(expression)
                                        break
                                    except:
                                        raise Exception()
                            elif prefix_operators_available[p] == 0: # если операторы с "0" в начале, то ошибка
                                if expression.find(p) == 0: # если выражение содержит * / % ^ в начале
                                    raise Exception()
                            else:
                                raise Exception() # во всех остальных случаях
                elif len(global_expression) != 0:
                    if global_expression[-1] in prefix_operators_available.keys(): # если слева операция    
                        try:
                            first = int(expression[0])
                            if type(first) == type(0): #если первый символ в вводе "цифра"
                                compile(expression,'<string>','exec')
                                global_expression.append(expression)
                        except:
                            if expression[0] == '(': #если первый символ в вводе "("
                                compile(expression,'<string>','exec')
                                global_expression.append(expression)
                            else:
                                raise Exception()
                    else: #  если слева цифра или ")"
                        try:
                            if len(expression) == 1 and expression[0] in prefix_operators_available.keys(): # значит передается только один из операторов
                                global_expression.append(expression)
                            elif len(expression) > 1 and expression[0] in prefix_operators_available.keys(): # значит передается строка с оператором вначале
                                oper = expression[0]
                                if prefix_operators_available[oper] == 0 or prefix_operators_available[oper] == 1: # если оператор вначале +-*/%^
                                    test = expression
                                    test = test[1:]
                                    compile(test,'<string>','exec')
                                    global_expression.append(expression)
                            else:
                                raise Exception()
                        except: 
                            raise Exception()
        try: 
            check_brackets(self.expression)
            check_repetitive_operations(self.expression)
            check2ways(self.expression,self.global_expression)
        except:
            self.errors(3)
           
    def __str__(self):
        if self.error == True:
            return "Expression: {} ; Error: {}".format(self.expression,self.error_message)
        
class Expression_summarize(String):
    def __init__(self,expression,global_expression): 
        super().__init__(expression,global_expression)
    
    def get_result(self,global_expression):

        def pop_put(i,c,expr,oper_stack,output_stack,num):
            '''
            Операция сохранения значения в стек и вывод из стека.
            Поддерживает + - * / % ^ () унарный минус(~) и унарный плюс(!)
            '''
            if i in self.operators or i in '()' or num in self.operators: # or num in self.operators:  # если это оператор или () или sin/cos
                if num in self.operators:
                    i = num
                if i == '(':
                    oper_stack.append(i)
                elif i == ')':
                    # 1) присоединить содержимое стека до скобки в обратном порядке к выходной строке; 2) удалить скобку из стека.
                    for token in reversed(oper_stack): # если опер == ), то выгружаем в output_stack все, что до (
                        if token != '(':
                            output_stack.append(oper_stack.pop())
                        else:
                            oper_stack.pop()
                            break
                else: # если любой другой оператор
                    if len(oper_stack) > 0:
                        if oper_stack[-1] == '(' and i == '-':
                            try:
                                int(expr[c-1]) # если пред.символ был цифрой, то не меняем - на ~
                                oper_stack.append(i)
                            except:
                                oper_stack.append('~')
                        elif oper_stack[-1] == '(' and i == '+':
                            try:
                                int(expr[c-1]) # если пред.символ был цифрой, то не меняем + на !
                                oper_stack.append(i)
                            except:
                                oper_stack.append('!')
                            
                        elif self.operators[i][0] <= self.operators[oper_stack[-1]][0]: # если приоритет этого оператора меньше предыдущего, то 
                            # 1) присоединить стек в обратном порядке к выходной строке; 2) поместить новую операцию в стек.
                            try:
                                while self.operators[i][0] <= self.operators[oper_stack[-1]][0]:
                                    output_stack.append(oper_stack.pop())
                                oper_stack.append(i)
                            except:
                                oper_stack.append(i)
                        else:
                            oper_stack.append(i) # иначе, первый кладем в oper_stack
                    elif len(oper_stack) == 0: # если стек пуст, то
                        if i == '-' and len(output_stack) == 0: # заменяем - на ~ (если первый символ в expr или + или -, т.е. унарные)
                            oper_stack.append('~')
                        elif i == '+' and len(output_stack) == 0: #заменяем + на !
                            oper_stack.append('!')
                        else:
                            oper_stack.append(i)
                            num = ''
            if c == len(expr)-1 and len(num) > 0:
                output_stack.append(num)

            return oper_stack,output_stack

        def translate(global_expression):   
            '''
            Переводит строку в ОПН
            '''
            expr = ''.join(global_expression)
            num = ''
            oper_stack = []
            output_stack = []
            for c,i in enumerate(expr):
                if i in '0123456789' or i in list(string.ascii_lowercase):
                    num += i
                elif len(num) > 0:
                    if num not in self.operators:
                        output_stack.append(num)
                        num = ''
                    else:
                        num = ''
                oper_stack,output_stack = pop_put(i,c,expr,oper_stack,output_stack,num)  # операция сохранения значения в стек и вывод из стека.
                
            while oper_stack:
                output_stack.append(oper_stack.pop())
            return output_stack

        def result(output):
            '''
            Вычисляет выражение в ОПН
            '''
            solution_stack = []
            for t,token in enumerate(output):
                try:
                    token = int(token)
                    solution_stack.append(token)
                except:
                    if self.operators[token][2] == 1: # если унарная операция
                        try:
                            if solution_stack[-1] not in self.operators:
                                x = solution_stack.pop()
                                rez = self.operators[token][1](x) 
                                solution_stack.append(rez)
                            else:
                                solution_stack.append(token)    
                        except:
                            solution_stack.append(token)

                    elif self.operators[token][2] == 2: # если бинарная операция
                        try:
                            x,y = solution_stack.pop(),solution_stack.pop()
                            rez = self.operators[token][1](y,x)
                            solution_stack.append(rez)
                        except:
                            solution_stack.append(token)
            return str(solution_stack[0])
                
        output = translate(global_expression)
        self.result = result(output)

    def __str__(self):
        return "Ans: {}".format(self.result)

def cycle():
    q = False
    global_expression = []
    while q == False: # пока выхода нет
        print(global_expression)
        expression = input("Enter expression: ")
        stri = String(expression,global_expression) # получает выражение
        stri, _type = stri.check_string() # убирает пробелы, узнает, выражение\комманда
        
        if _type == 'Command':
            stri = Command(stri,global_expression)
            state = stri.execute_command()
            if state == True:
                q = True
            elif state == False:
                stri = Expression_summarize(stri,global_expression)
                stri.get_result(global_expression)
                print(stri)
                global_expression = []
            else:
                pass
        else:
            stri = Expression(stri,global_expression)
            stri.check_put_string()        
            try:
                print(stri) # ошибка, вернется в начало
            except:
                pass     
cycle()