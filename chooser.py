class Choose():
    def __init__(self,expression):
        self.expression = expression
        self.all_commands = {'=':'=','C':'C','clear':'clear','MC':'MC','MR':'MR','M+':'M+','M-':'M-','Q':'Q'}

    def choose_way(self):
        if self.expression in self.all_commands:
            decision = 'Command'
            return decision
        else:
            decision = 'Expression'
            return decision