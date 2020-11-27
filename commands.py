from RPN import State
from solver import Resulter

class DeleteLast():
    def __init__(self,global_expression):
        self.global_expression = global_expression
    def execute_command(self):
        try:
            self.global_expression = self.global_expression[:-1]
            return self.global_expression
        except:
            return self.global_expression

class DeleteAll():
    def __init__(self,global_expression):
        self.global_expression = global_expression
    def execute_command(self):
            self.global_expression = []
            print(self.global_expression)
            return self.global_expression

class Quit():
    def __init__(self,q):
        self.q = q
    def execute_command(self):
            self.q = True
            return self.q

class MPlus():
    def __init__(self,global_expression,memory):
        self.global_expression = global_expression
        self.memory = memory
    def execute_command(self):
        try:
            print(self.global_expression)
            mem_v, self.global_expression = last_int(self.global_expression)
            self.memory[0] += mem_v
            print(self.global_expression)
            return self.memory, self.global_expression
        except :return self.memory, self.global_expression

class MMinus():
    def __init__(self,global_expression,memory):
        self.global_expression = global_expression
        self.memory = memory
    def execute_command(self):
        try:
            print(self.global_expression)
            mem_v, self.global_expression = last_int(self.global_expression)
            self.memory[0] -= mem_v
            print(self.global_expression)
            return self.memory, self.global_expression
        except :return self.memory, self.global_expression

class MC():
    def __init__(self,memory):
        self.memory = memory
    def execute_command(self):
        self.memory = [0]
        return self.memory

class MR():
    def __init__(self,memory):
        self.memory = memory
    def execute_command(self):
        print('Memory:', self.memory)

class EQUAL():
    def __init__(self,global_expression,result):#,memory,rezult):
        self.global_expression = global_expression
        self.result = result #!

    def execute_command(self):
        result = State(self.global_expression) # обратная польская нотация
        result = result.parse()
        #print(result)
        result = Resulter(result)
        result = result.solve()
        self.global_expression = []
        self.global_expression.append(result)
        print('Rez: ',result)
        return result,self.global_expression

def last_int(global_expression):
    '''
    Берет последнее число из кеша
    '''
    try:
        global_expression = ''.join(global_expression)
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
    except:
        mem_v = global_expression.pop()
        return mem_v, global_expression