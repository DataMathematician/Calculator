import string
from math import sin,cos,radians

class String():
    def __init__(self,expression,global_expression):
        self.expression = expression
        self.global_expression = global_expression
        self.commands = {'=':'=','C':'C','clear':'clear','Q':'Q'}
        self.operators = {'+':(1, lambda x,y: x + y, 2),
                '-':(1, lambda x,y: x - y, 2),
                '~':(2,lambda x: x * -1,1),
                '!':(2,lambda x: x, 1),  
                '*':(3, lambda x,y: x * y, 2),
                '/':(3, lambda x,y: x / y, 2),
                '%':(3, lambda x,y: x % y, 2),
                '^':(4, lambda x,y: x ** y, 2),
                'sin':(5, lambda x: sin(radians(x)), 1),
                'cos':(5, lambda x: cos(radians(x)), 1),
                '(':(0, None,0),
                ')':(-1, None,0)}
        self.error = False
        self.error_message = ''
        self.results = 0

class Expression_summarize(String):
    def __init__(self,expression,global_expression): 
        super().__init__(expression,global_expression)
    
    
    def get_result(self,global_expression):

        def pop_put(i,c,expr,oper_stack,output_stack,num):
            '''
            Операция сохранения значения в стек и вывод из стека.
            Поддерживает + - * / % ^ () унарный минус(~) и унарный плюс(!)
            '''
            if i in self.operators or i in '()' or num in self.operators: # если это оператор или () или sin/cos
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
                    #if num in self.operators: # если это sin/cos
                    #    output_stack.append(num)
                    #    num = ''    
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
                    #token = output[t]
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
        print(output)
        rez = result(output)
        return rez
    
global_expression = '(8+2*5)/(1+3*2-4)' #'-cos(sin(7-6))'
stri = Expression_summarize('rt',global_expression)
rez = stri.get_result(global_expression)
print(rez)