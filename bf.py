"""
Brainf**k VM Emulator
"""
from collections import defaultdict


class BrainFuck:
    """
    Emulates a Brainf**k VM.
    """

    def __init__(self):
        self.cell = defaultdict(lambda: 0)
        self.p = 0
        self.command = ""
        self.pos = 0
        self.matches = {}

    def load(self, code, input=""):
        self.cell = defaultdict(lambda: 0)
        self.command = code
        self.pos = 0
        self.p = 0
        self.matches = {}
        self.input = list(reversed(input.encode()))
        self.output = ""
        stack = []
        for i, j in enumerate(self.command):
            if j == "[":
                stack.append(i)
            if j == "]":
                if not stack:
                    raise Exception("Unmatched ] at char " + str(i))
                par = stack.pop()
                self.matches[par] = i
                self.matches[i] = par
        if stack:
            raise Exception("Unmatched [ at char " + str(stack[-1]))

    def step(self):
        cmd = self.command[self.pos]
        f = False
        if cmd == "#":
            f = True
        if cmd == "+":
            self.cell[self.p] += 1
            self.cell[self.p] %= 256
        if cmd == "-":
            self.cell[self.p] -= 1
            self.cell[self.p] %= 256
        if cmd == "<":
            self.p -= 1
        if cmd == ">":
            self.p += 1
        if cmd == ",":
            if not self.input:
                self.cell[self.p] = 0
                self.pos += 1
                return
            input = self.input.pop()
            self.cell[self.p] = input
        if cmd == ".":
            self.output += chr(self.cell[self.p])
        if cmd == "[":
            if self.cell[self.p] == 0:
                self.pos = self.matches[self.pos] - 1
        if cmd == "]":
            if self.cell[self.p] != 0:
                self.pos = self.matches[self.pos] - 1
        self.pos += 1
        return f

    def running(self):
        return self.pos < len(self.command)
