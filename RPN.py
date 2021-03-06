import operators
import string

class State:
    '''текущее состояние анализатора'''
    state_handlers = {
        's_open': ('h_open', 'h_num','h_uno_op','h_tgm'), # начальное состояние  (открывающая скобка либо число)
        's_close': ('h_close', 'h_op','h_spec'), # состояние (закрывающая скобка либо операция)
        's_tgm': ('h_open',)
    }

    state_map = {
        'h_open': 's_open',   # (
        'h_num': 's_close',   # 1,2,3,...
        'h_op': 's_open',     # +,-,*,/,...
        'h_close': 's_close', # )
        'h_uno_op':'s_open',  # !,~
        'h_tgm':'s_tgm',      # sin/cos
        'h_spec':'s_open'     # @
    }

    def __init__(self, expr):
        self.src = ''.join(expr) # разбираемая строка 
        self.mode = 's_open' # первичное состояние 
        self.pos = 0 # текущая позиция в строке
        self.parsed = [] # список разобранных элементов # str ""
        self.out = []
        self.opers = []

    def parse(self):
        while self.pos < len(self.src): # пробеагаемся по каждому символу
            ok = False
            for handler_name in State.state_handlers[self.mode]: # при нынешнем состоянии для каждого возможного символа пробуем выполнить его класс 
                handler = Handler.getHandler(handler_name) # берем класс возможного состояния
                ok = handler.parse(self) # выполняем его метод parse
                if ok:     # если метод сработал, то 
                    Out_list.put2out(handler_name,self)
                    self.mode = State.state_map[handler_name] # состояние обновляется на новое и переходим к нему
                    break
            if not ok:     # если ни один метод состояния не сработал, то заканчиваем работу
                break

        while len(self.parsed) != 0:
            item = self.parsed.pop()
            if item not in '()':
                self.out.append(item)
        return self.out


class Out_list():
    @staticmethod
    def put2out(handler_name,state):
        if handler_name == 'h_num':
            state.out.append(state.parsed.pop())
        elif handler_name == 'h_open':
            pass
        elif handler_name == 'h_close':
            q = False
            while q == False:
                op = state.parsed.pop()
                if op == '(':
                    q = True
                else:
                    state.out.append(op)
        else: 
                q = False
                while q == False:
                    op_last = state.parsed[-1]
                    try:
                        op_before_last = state.parsed[-2]
                        if operators.Operations.all_operations[op_last].priority < operators.Operations.all_operations[op_before_last].priority:
                            state.out.append(state.parsed.pop(len(state.parsed)-2))
                        elif operators.Operations.all_operations[op_last].priority >= operators.Operations.all_operations[op_before_last].priority:
                            q = True
                    except:
                        q = True



class Handler:
    def __init__(self):
        self.value = ''

    @staticmethod
    def getHandler(name):
        if name == 'h_open':
            return OpenHandler()
        elif name == 'h_op':
            return OpHandler()
        elif name == 'h_num':
            return NumHandler()
        elif name == 'h_close':
            return CloseHandler()
        elif name == 'h_uno_op':
            return UnoOperation()
        elif name == 'h_tgm':
            return TgmHandler()
        print('Невозможно вычислить!')
        raise Exception()

    def parse(self, state):
        result = False
        while state.pos < len(state.src):   # пока не достигнем конца строки
            if self.check(state.src[state.pos], state): # если метод check(текущий символ, состояние)
                result = True   # возвращает результат (сработал метод), result = True
                state.pos += 1  # и переходим к следующей позиции в строке
            else:
                break           # если метод не сработал то выходим из цикла (вернул False)
        if self.value:       # Если value не пустое (в него были добавленны числа, буквы)
            state.parsed.append(self.value) # то в выходной стек кидаем то, что в value
            self.value = '' # и сбрасываем value # value может быть знаком, буквой,числом

        return result   # вернет True - состояние обновится, False - состояние не обновится

class UnoOperation(Handler):
    def check(self,char,state):
        if char in operators.Operations.all_operations:
            if char == '+':char = '!'
            elif char == '-':char = '~'
            print(char)
            self.value = char
            return True
        return False


class OpenHandler(Handler):
    def check(self, char, state):
        if char == '(':
            self.value = '('
            return True
        return False

class CloseHandler(Handler):
    def check(self, char, state):
        if char == ')':
            return True
        return False

class OpHandler(Handler):
    def check(self, char, state):
        if char in operators.Operations.all_operations and char != '(':
            self.value = char # пусть возвращает только знак
            return True
        return False

class NumHandler(Handler):
    def check(self, char, state):
        if char in '0123456789':
            self.value += char
            return True
        return False

class TgmHandler(Handler):
    '''Комбинирует буквы в литерал (sin,cos),
    на данном этапе необязательно триганометрический'''
    def check(self,char,state):
        if char in list(string.ascii_lowercase):
            self.value += char
            return True
        return False