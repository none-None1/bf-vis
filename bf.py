"""
Brainf**k VM Emulator
"""
class BrainFuck():
    """
    Emulates a Brainf**k VM.
    """
    def __init__(self):
        self.cell=[0]*300000
        self.p=0
        self.command=''
        self.pos=0
        self.matches={}
    def load(self,code,input=''):
        self.cell = [0] * 300000
        self.command=code
        self.pos=0
        self.p = 0
        self.matches={}
        self.input=list(input.encode())
        self.output=''
        stack=[]
        for i,j in enumerate(self.command):
            if j == '[':
                stack.append(i)
            if j==']':
                if not stack:
                    raise Exception('Unmatched ] at char '+str(i))
                par=stack.pop()
                self.matches[par]=i
                self.matches[i] = par
        if stack:
            raise Exception('Unmatched [ at char '+str(stack[-1]))
    def step(self):
        cmd=self.command[self.pos]
        if cmd == '+':
            self.cell[self.p]+=1
            self.cell[self.p] %= 256
        if cmd == '-':
            self.cell[self.p] -= 1
            self.cell[self.p] %= 256
        if cmd=='<':
            if self.p==0:
                raise Exception('Cannot move to left of origin')
            self.p-=1
        if cmd=='>':
            self.p+=1
        if cmd==',':
            if not self.input:
                self.cell[self.p] =255
                self.pos+=1
                return
            input=self.input.pop(0)
            self.cell[self.p]=input
        if cmd=='.':
            self.output+=chr(self.cell[self.p])
        if cmd=='[':
            if self.cell[self.p]==0:
                self.pos=self.matches[self.pos]-1
        if cmd==']':
            if self.cell[self.p]!=0:
                self.pos=self.matches[self.pos]-1
        self.pos+=1
    def running(self):
        return self.pos<len(self.command)
