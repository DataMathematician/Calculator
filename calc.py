import re


class String():
    def __init__(self,expression,global_expression):
        self.expression = expression
        self.global_expression = global_expression
        self.commands = {'=':'=','C':'C','clear':'clear','Q':'Q'}
        self.operators = {'+':(1, lambda x,y: x + y),
                          '-':(1, lambda x,y: x - y),  
                          '*':(2, lambda x,y: x * y),
                          '/':(2, lambda x,y: x / y),
                          '%':(2, lambda x,y: x % y),
                          '^':(3, lambda x,y: x ** y)}


        self.error = False
        self.error_message = ''
        self.results = 0
        
    def check_string(self):
        '''
        Убирает пробелы, узнает выражение\комманда
        '''
        self.expression = self.expression.replace(' ','')
        if self.expression in self.commands.keys(): # если поступила комманда
            return self.expression, 'Command'
        else:
            return self.expression, 'Expression'
        
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
        prefix_operators_available = {'+':1, '-':1, '^':0, '/':0, '%':0, '*':0}

        def check_brackets(expression):
            '''
            Если подается только "(" или ")", то ошибка
            Если кол-ва скобок не равны, то ошибка
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

        def translate(global_expression):
            expr = ''.join(global_expression)
            num = ''
            for i in expr:
                if i in '0123456789':
                    num += i
                elif num:
                    yield int(num)
                    num = ''
                if i in self.operators or i in '()':
                    yield i
            if num:
                yield int(num)

        def stack_pol(equasion):
            stack = []
            for token in equasion:
                if token in self.operators:
                    while stack and stack[-1] != "(" and self.operators[token][0] <= self.operators[stack[-1]][0]:
                       yield stack.pop()
                    stack.append(token)
                elif token == ')':
                    while stack:
                        x = stack.pop()
                        if x == '(':
                            break
                        yield x
                elif token == '(':
                    stack.append(token)
                else:
                    yield token
            while stack:
                yield stack.pop()

        def rezult(stack_polish):
            stack = []
            for token in stack_polish:
                if token in self.operators:
                    y,x = stack.pop(),stack.pop()
                    stack.append(self.operators[token][1](x,y))
                else: 
                    stack.append(token)
            return stack[0]
        
        self.results = rezult(stack_pol(translate(self.global_expression))) 
        
    def __str__(self):
        if self.error == True:
            return "Expression: {} ; Error: {}".format(self.expression,self.error_message)
        else:
            return str(self.results)


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
