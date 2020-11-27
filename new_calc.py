from chooser import Choose
import commands

class Inp_Strinig():
    '''Абстракция введенной строки'''
    def __init__(self,expression):
        self.expression = expression
        self.choose = Choose(self.expression)

    def replace_spaces(self):
        self.expression = self.expression.replace(' ','')
    
    
class Calculator():
    '''Абстракция калькулятора'''
    def __init__(self):
        self.memory = [0]
        self.q = False
        self.global_expression = []
        self.result = None

class Commands():
    '''Абстракция комманд калькулятора '''
    def __init__(self):
        self.cmd_C = commands.DeleteLast(calculator.global_expression)
        self.cmd_clear = commands.DeleteAll(calculator.global_expression)
        self.cmd_quit = commands.Quit(True)
        self.cmd_M_plus = commands.MPlus(calculator.global_expression,calculator.memory)
        self.cmd_M_minus = commands.MMinus(calculator.global_expression,calculator.memory)
        self.cmd_MC = commands.MC(calculator.memory)
        self.cmd_MR = commands.MR(calculator.memory)
        self.cmd_EQUAL = commands.EQUAL(calculator.global_expression,calculator.result)


if __name__ == "__main__":
    calculator = Calculator()
    #calculator.main()
    while calculator.q == False:
        print(calculator.global_expression)
        ex = Inp_Strinig(input('Ex: '))
        ex.replace_spaces()
        way = ex.choose.choose_way()
        if way == 'Command':
            cmd = Commands()
            if ex.expression == 'C':
                calculator.global_expression = cmd.cmd_C.execute_command() 
            elif ex.expression == 'clear':
                calculator.global_expression = cmd.cmd_clear.execute_command() 
            elif ex.expression == 'Q':
                calculator.q = calculator. cmd.cmd_quit.execute_command() 
            elif ex.expression == 'M+':
                calculator.memory,calculator.global_expression = cmd.cmd_M_plus.execute_command()
                print(calculator.memory)
            elif ex.expression == 'M-':
                calculator.memory,calculator.global_expression = cmd.cmd_M_minus.execute_command()
            elif ex.expression == 'MC':
                calculator.memory = cmd.cmd_MC.execute_command()
            elif ex.expression == 'MR':
                calculator.memory = cmd.cmd_MR.execute_command()
            elif ex.expression == '=':
                calculator.result,calculator.global_expression = cmd.cmd_EQUAL.execute_command()
                #print(calculator.global_expression)
                
            
        elif way == 'Expression':
            calculator.global_expression.append(ex.expression)



#def main(self):
    #""" Основная логика работы калькулятора """
    #while self.q == False:
    #    ex = Inp_Strinig(input('Ex: '))
    #    ex.replace_spaces()
    #    way = ex.choose.choose_way()
    #    if way == 'Command':
    #        if ex.expression == 'C':
    #            self.global_expression = self.cmd_C.execute_command()
    #            #self.global_expression = ex.cmd.execute_command(self.global_expression)
    #        
    #        
    #    elif way == 'Expression':
    #        self.global_expression.append(ex.expression)

            #expression = input('Ex: ') # получаем введенное выражение

            #decision = Choose(expression)
            #decision = decision.choose_way()
    #
            #if decision == 'Command': # если введенное выражение - комманда
            #    try:
            #        command_obj = Commands(expression)
            #        command_obj.execute_command()
            #    except :
            #        self.global_expression = []
            #elif  decision == 'Expression': # если введенное выражение - выражение (5-32*2, 4, %,...)
            #    expression = expression.replace(' ','')
            #    self.global_expression.append(expression)
            #    print(self.global_expression)
