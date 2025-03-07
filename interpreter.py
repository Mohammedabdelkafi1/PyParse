x = input("Xinter ==> ")
PLUS = "PLUS"
MINUS = "MINUS"
DIV = "DIVISION"
MUL = "MULTIPLICATION"
nums = "1234567890"
OPAREN = "LPAREN"
CPAREN = "RPAREN"
letters = "azertyuiopqsdfghjklmwxcvbn"
illegalchars="ã░☻╚æ"
string=False
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.curr_char = None
        self.tokens = []
        self.advance()

    def advance(self):
        self.pos += 1
        self.curr_char = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        while self.curr_char is not None:
            if self.curr_char in illegalchars:
                raise ValueError(f'Unexpected Character: {self.curr_char}')
            elif self.curr_char.isspace():
                self.advance()
            elif self.curr_char == "+":
                self.tokens.append(PLUS)
                self.advance()
            elif self.curr_char == "-":
                self.tokens.append(MINUS)
                self.advance()
            elif self.curr_char == "/":
                self.tokens.append(DIV)
                self.advance()
            elif self.curr_char == "*":
                self.tokens.append(MUL)
                self.advance()
            elif self.curr_char == "(":
                self.tokens.append(OPAREN)
                self.advance()
            elif self.curr_char == ")":
                self.tokens.append(CPAREN)
                self.advance()
            elif self.curr_char=="=":
                self.tokens.append("EQUALS")
                self.advance()
            elif self.curr_char in letters and string==False:
                self.tokens.append(self._parse_stmt())
            elif self.curr_char in nums or self.curr_char == ".":
                self.tokens.append(self._parse_number())
            else:
                raise ValueError(f"Unexpected character: {self.curr_char}")
        return self.tokens

    def _parse_number(self):
        num_str = ""
        dots = 0
        while self.curr_char is not None and (self.curr_char in nums or self.curr_char == "."):
            if self.curr_char == ".":
                if dots == 1:
                    raise ValueError("Invalid number format: Too many dots in number")
                dots += 1
            num_str += self.curr_char
            self.advance()

        if dots == 0:
            return int(num_str)
        else:
            return float(num_str)

    def _parse_stmt(self):
        stmt_str = ""
        while self.curr_char is not None and self.curr_char in letters:
            stmt_str += self.curr_char
            self.advance()
        return stmt_str 
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.curr_token = None
        self.advance()

    def advance(self):
        self.index += 1
        self.curr_token = self.tokens[self.index] if self.index < len(self.tokens) else None
    def parse(self):
        while self.curr_token is not None:
            self.expr()
            self.term()
            self.Print()
            self.advance()
        return self.tokens
    def Print(self):
        if self.curr_token == "log":
            content= self.tokens[self.index+1]
            print(content)
    def term(self):
        if self.curr_token == PLUS:
            left_num = self.tokens[self.index - 1]
            right_num = self.tokens[self.index + 1]
            result = left_num + right_num
            self.tokens = self.tokens[:self.index - 1] + [result] + self.tokens[self.index + 2:]
            self.index -= 1
        elif self.curr_token == MINUS:
            left_num = self.tokens[self.index - 1]
            right_num = self.tokens[self.index + 1]
            result = left_num - right_num
            self.tokens = self.tokens[:self.index - 1] + [result] + self.tokens[self.index + 2:]
            self.index -= 1
    def expr(self):
        if self.curr_token == MUL:
            left_num = self.tokens[self.index - 1]
            right_num = self.tokens[self.index + 1]
            result = left_num * right_num
            self.tokens = self.tokens[:self.index - 1] + [result] + self.tokens[self.index + 2:]
            self.index -= 1
        if self.curr_token == DIV:
            left_num = self.tokens[self.index - 1]
            right_num = self.tokens[self.index + 1]
            result = left_num / right_num
            self.tokens = self.tokens[:self.index - 1] + [result] + self.tokens[self.index + 2:]
            self.index -= 1
lexer = Lexer(x)
tokens = lexer.tokenize()
parser = Parser(tokens)
result = parser.parse()
print(result)
