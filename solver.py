import operators

class Resulter:
    def __init__(self,rpn):
        self.rpn = rpn
        self.solution_stack = []
        self.oper_token = ''
        self.t = 0
        self.token = ''

    def solve(self):
        for self.t,self.token in enumerate(self.rpn):
            self.token = IsInt.num(self.token)
            if type(self.token) == type(0):
                self.solution_stack = Appender.execute(self.token,self.solution_stack)

            elif operators.Operations.all_operations[self.token].n_nums == 1: # для унарных
                self.solution_stack =  Uno_operations.solve_token(self.token,self.solution_stack)
            elif operators.Operations.all_operations[self.token].n_nums == 2: # для бинарных
                self.solution_stack =  Dos_operations.solve_token(self.token,self.solution_stack)
            elif operators.Operations.all_operations[self.token].n_nums == 3: # для тринарных
                self.solution_stack,self.oper_token =  Tres_operations.solve_token(self.token,self.solution_stack,self.oper_token)
        return self.solution_stack[0]

class IsInt():
    @staticmethod
    def num(token):
        try:
            token = int(token)
            return token
        except:
            return token
            
class Appender():
    @staticmethod
    def execute(token,solution_stack):
        solution_stack.append(token)
        return solution_stack

class Uno_operations():
    
    @staticmethod
    def solve_token(token,solution_stack):
        try:
            if solution_stack[-1] not in operators.Operations.all_operations:
                x = solution_stack.pop()
                rez = operators.Operations.all_operations[token]
                rez.x = x
                rez = rez.solve()
                solution_stack = Appender.execute(rez,solution_stack)
                return solution_stack
            else:
                solution_stack = Appender.execute(token,solution_stack)
                return solution_stack
        except:
            solution_stack = Appender.execute(token,solution_stack)
            return solution_stack

class Dos_operations:

    @staticmethod
    def solve_token(token,solution_stack):
        try:
            x,y = solution_stack.pop(),solution_stack.pop()
            rez = operators.Operations.all_operations[token]
            rez.x = y
            rez.y = x
            rez = rez.solve()
            solution_stack = Appender.execute(rez,solution_stack)
            return solution_stack
        except:
            solution_stack = Appender.execute(token,solution_stack)
            return solution_stack

class Tres_operations:

    @staticmethod
    def solve_token(token,solution_stack,oper_token):
        try:
            if len(oper_token) == 0:
                oper_token += token
                return solution_stack,oper_token
            else:
                oper_token += token
                x,y,z = solution_stack.pop(),solution_stack.pop(),solution_stack.pop()
                rez = operators.Operations.all_operations[oper_token]
                rez.x = z
                rez.y = y
                rez.z = x
                rez = rez.solve()
                solution_stack = Appender.execute(rez,solution_stack)
                return solution_stack,oper_token
        except:
            solution_stack = Appender.execute(token,solution_stack)
            return solution_stack,oper_token