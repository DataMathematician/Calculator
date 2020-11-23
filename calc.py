from math import sin,cos,radians
import string

class String():
    def __init__(self,expression):
        self.expression = expression

    def check_string(self):
        '''
        Убирает пробелы, узнает что подано на вход: выражение\комманда
        '''
        if self.expression in Command.commands: # если поступила комманда
            return 'Command'
        else:
            return 'Expression'    # если выражение 

class Command():
    commands = {'=':'=','C':'C','clear':'clear','MC':'MC','MR':'MR','M+':'M+','M-':'M-','Q':'Q'}
    def __init__(self,expression,global_expression,memory,result):
        self.expression = expression
        self.global_expression = global_expression
        self.memory = memory
        self.result = result
        self.error_message = ''
        self.error = False

    def last_int(global_expression):
        '''
        Берет последнее число из кеша
        '''
        global_expression = ''.join(global_expression[0])
        num = ''
        for c,i in enumerate(reversed(global_expression)):
            if i in '.0123456789':
                num+=i
            elif len(num) > 0:
                mem_v = ''.join(reversed(num))
                mem_v = float(mem_v)
                global_expression = global_expression[:-c]
                return mem_v, global_expression
            else:continue
        if len(num) > 0:
            mem_v = ''.join(reversed(num))
            mem_v = float(mem_v)
            global_expression = global_expression[:-c]
            return mem_v, global_expression
        else:
            mem_v = 0
            return mem_v, global_expression
            
    def execute_command(self):
        try:
            if self.expression == Command.commands['C']:
                try:
                    self.global_expression.pop()
                except: pass

            elif self.expression == Command.commands['M+']:
                try:
                    mem_v, self.global_expression = Command.last_int(self.global_expression)
                    self.memory[0] += mem_v
                    #print(self.global_expression)
                except: pass


            elif self.expression == self.commands['M-']:
                try:
                    mem_v, self.global_expression = Command.last_int(self.global_expression)
                    self.memory[0] -= mem_v
                except: pass

            elif self.expression == self.commands['MR']:
                print('Memory: ',self.memory[0])

            elif self.expression == self.commands['MC']:
                self.memory[0] = [0]

            elif self.expression == self.commands['clear']:
                while len(self.global_expression) != 0:
                    self.global_expression.pop()
                return 'NtR',Command.memory,Command.global_expression

            elif self.expression == self.commands['=']:
                rez = ExpressionSummarize(self.expression,self.global_expression,self.memory,self.result)
                self.result,self.memory,self.global_expression = rez.get_result()
                print("rez:",self.result)
                return self.result,self.memory,self.global_expression

            elif self.expression == self.commands['Q']:
                return True,Command.memory,Command.global_expression
        except :
            raise Exception()

class ExpressionSummarize(Command):
    def __init__(self,expression,global_expression,memory,result):
        Command.__init__(self,expression,global_expression,memory,result)
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
                          '(':(-1, None,0),
                          '@':(0,None,3),
                          '@@':(0, lambda x,y,z: x*z + z*y,3)} # тринарное действие


    def get_result(self):

        def pop_put(i,c,expr,oper_stack,output_stack,num):
            '''
            Операция сохранения значения в стек и вывод из стека.
            Поддерживает + - * / % ^ () унарный минус(~) и унарный плюс(!)
            '''
            try:
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
                    elif self.operators[i][2] == 3 and i in oper_stack:
                        while self.operators[i][0] < self.operators[oper_stack[-1]][0]:
                            output_stack.append(oper_stack.pop())
                        oper_stack.append(i)

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
            except :
                print('Ошибка стека')
                raise Exception()

        def translate(global_expression):   
            '''
            Переводит строку в ОПН
            '''
            expr = ''.join(global_expression)
            try:
                compile(expr,'<string>','exec')
                num = ''
                oper_stack = []
                output_stack = []
                for c,i in enumerate(expr):
                    if i in '.0123456789' or i in list(string.ascii_lowercase):
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
            except :
                print('Ошибка выражения')
                raise Exception()
                

        def result(output):
            '''
            Вычисляет выражение в ОПН
            '''
            try:
                solution_stack = []
                oper_stack = ''
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
                        elif  self.operators[token][2] == 3 and len(oper_stack) == 0: # если тринарная операция
                            oper_stack += token
                        elif  self.operators[token][2] == 3 and len(oper_stack) != 0: # если тринарная операция
                            oper_stack += token
                            x,y,z = solution_stack.pop(),solution_stack.pop(),solution_stack.pop()
                            rez = self.operators[oper_stack][1](z,y,x)
                            oper_stack = ''
                            solution_stack.append(rez)

                return str(solution_stack[0])
            except :
                print('Невозможно вычислить')
                raise Exception()
        
        try:
            if self.global_expression[-1] in self.operators:
                self.global_expression = global_expression[:-1]
            output = translate(self.global_expression)
            self.result = result(output)
            self.global_expression = []
            self.global_expression.append(self.result)
    
            return self.result,self.memory,self.global_expression
        except:
            raise Exception()


def cycle():
    q = False
    global_expression = [] # cashe
    memory = [0]
    result = 0
    while q == False: # пока выхода нет

        print("\nExpression: ",global_expression) 
        #print(memory)
        expression = input("Enter expression: ")
        decision = String(expression)
        decision = decision.check_string()

        if decision == 'Command':
            try:
                obj = Command(expression,global_expression,memory,result)
                result,memory,global_expression = obj.execute_command()
                if result == True:
                    q = True
                if result == 'NtR':
                    continue
            except:
                global_expression = []
                continue
        elif decision == 'Expression':
            expression = expression.replace(' ','')
            global_expression.append(expression)


if __name__ == "__main__":
    cycle()