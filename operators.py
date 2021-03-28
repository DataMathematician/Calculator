from math import sin,cos,radians

class Plus():
    def __init__(self,x = None,y = None):
        self.x = x
        self.y = y
        self.priority = 1
        self.n_nums = 2 # бинарный оператор 

    def solve(self):
        return self.x + self.y
        
class Minus():
    def __init__(self,x = None,y = None):
        self.x = x
        self.y = y
        self.priority = 1
        self.n_nums = 2 # бинарный оператор 

    def solve(self):
        return self.x - self.y

class Mul():
    def __init__(self,x = None,y = None):
        self.x = x
        self.y = y
        self.priority = 3
        self.n_nums = 2 # бинарный оператор 

    def solve(self):
        return self.x * self.y

class Div():
    def __init__(self,x = None,y = None):
        self.x = x
        self.y = y
        self.priority = 3
        self.n_nums = 2 # бинарный оператор 

    def solve(self):
        return self.x / self.y
    
class Mod():
    def __init__(self,x = None,y = None):
        self.x = x
        self.y = y
        self.priority = 3
        self.n_nums = 2 # бинарный оператор 

    def solve(self):
        return self.x % self.y

class Pow():
    def __init__(self,x = None,y = None):
        self.x = x
        self.y = y
        self.priority = 4
        self.n_nums = 2 # бинарный оператор 

    def solve(self):
        return self.x ** self.y

class Uno_Plus():
    def __init__(self,x = None):
        self.x = x
        self.priority = 2
        self.n_nums = 1 # унарный оператор 

    def solve(self):
        return self.x

class Uno_Minus():
    def __init__(self,x = None):
        self.x = x
        self.priority = 2
        self.n_nums = 1 # унарный оператор 

    def solve(self):
        return self.x * -1

class Open_Round_Br():
    def __init__(self):
        self.priority = -1

class MSin():
    def __init__(self,x=None):
        self.x = x
        self.priority = 5
        self.n_nums = 1
    def solve(self):
        return sin(radians(self.x))

class MCos():
    def __init__(self,x=None):
        self.x = x
        self.priority = 5
        self.n_nums = 1
    def solve(self):
        return cos(radians(self.x))     

class TripleMul():
    def __init__(self,x = None,y = None,z = None):
        self.x = x
        self.y = y
        self.z = z
        self.priority = 0
        self.n_nums = 3
    def solve(self):
        return self.x * self.z + self.z * self.y

class Operations(): #можно убрать класс...
    all_operations = {'+': Plus(),
                      '-': Minus(),
                      '*': Mul(),
                      '/': Div(),
                      '%': Mod(),
                      '^': Pow(),
                      '!': Uno_Plus(),
                      '~': Uno_Minus(),
                      '(': Open_Round_Br(),
                      'sin': MSin(),
                      'cos': MCos(),
                      '@':TripleMul(),
                      '@@':TripleMul()}