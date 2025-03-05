x = input("Xinter >")
src = list(x)
nums = "1234567890"
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
class Lexer:
    def __init__(self):
        self.pos = -1
        self.tokens = []
    def advance(self):
        self.pos+=1
        self.curr_char = src[self.pos]
        
