import string
from math import sin,cos,radians
global_expression = 'cos(sin(+7-6))'


operators = {'+':(1, lambda x,y: x + y, 2),
                '-':(1, lambda x,y: x - y, 2),
                '`':(1,lambda x: x * -1,1),
                '!':(1,lambda x: x,1),  
                '*':(2, lambda x,y: x * y, 2),
                '/':(2, lambda x,y: x / y, 2),
                '%':(2, lambda x,y: x % y, 2),
                '^':(3, lambda x,y: x ** y, 2),
                'sin':(4, lambda x: sin(radians(x)), 1),
                'cos':(4, lambda x: cos(radians(x)), 1)}


def translate(global_expression):
    '''
    Разбивает на токены
    '''
    expr = ''.join(global_expression)
    num = ''
    for i in expr:
        if i in '0123456789' or i in list(string.ascii_lowercase):
            num += i
        elif num:
            yield num
            num = ''
        if i in operators or i in '()':
            yield i
    if num:
        yield num

def stack_pol(equasion):
    stack = []
    for token in equasion:
        if token in operators:
            while stack and stack[-1] != "(" and operators[token][0] <= operators[stack[-1]][0]:
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
            yield int(token) # Если пришло число
    while stack:
        yield stack.pop()

def rezult(stack_polish):
    stack = []
    for token in stack_polish:
        if token in operators:
            if operators[token][2] == 1:
                x = stack.pop()
                stack.append(operators[token][1](x))
            elif operators[token][2] == 2:
                    y = stack.pop()
                    x = stack.pop()
                    stack.append(operators[token][1](x,y))
                
                    
        else: 
            stack.append(token) # добавление числа в стек
    return stack[0]  

rezults = rezult(stack_pol(translate(global_expression)))
print(rezults)
