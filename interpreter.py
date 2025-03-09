# Credits to Dripkap and stier for being my first stars
x = input("PyParse > ")

PLUS = "PLUS"
MINUS = "MINUS"
DIV = "DIVISION"
MUL = "MULTIPLICATION"
OPAREN = "LPAREN"
CPAREN = "RPAREN"
EQUALS = "EQUALS"
NUMBER = "NUMBER"
STRING = "STRING"
LOG = "LOG"

nums = "1234567890"
letters = "abcdefghijklmnopqrstuvwxyz"
illegalchars = "ã░☻╚æ"

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
                self.tokens.append((PLUS, "+"))
                self.advance()
            elif self.curr_char == "-":
                self.tokens.append((MINUS, "-"))
                self.advance()
            elif self.curr_char == "/":
                self.tokens.append((DIV, "/"))
                self.advance()
            elif self.curr_char == "*":
                self.tokens.append((MUL, "*"))
                self.advance()
            elif self.curr_char == "(":
                self.tokens.append((OPAREN, "("))
                self.advance()
            elif self.curr_char == ")":
                self.tokens.append((CPAREN, ")"))
                self.advance()
            elif self.curr_char == "=":
                self.tokens.append((EQUALS, "="))
                self.advance()
            elif self.curr_char in letters:
                self.tokens.append(self._parse_stmt())
            elif self.curr_char in nums or self.curr_char == ".":
                self.tokens.append((NUMBER, self._parse_number()))
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
        if stmt_str == "log":
            return (LOG, stmt_str)
        else:
            return (STRING, stmt_str)

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
        result = self.expr()
        if self.curr_token is not None:
            raise ValueError("Unexpected token at end of input")
        return result

    def expr(self):
        result = self.term()
        while self.curr_token is not None and self.curr_token[0] in (PLUS, MINUS):
            if self.curr_token[0] == PLUS:
                self.advance()
                result += self.term()
            elif self.curr_token[0] == MINUS:
                self.advance()
                result -= self.term()
        return result

    def term(self):
        result = self.factor()
        while self.curr_token is not None and self.curr_token[0] in (MUL, DIV):
            if self.curr_token[0] == MUL:
                self.advance()
                result *= self.factor()
            elif self.curr_token[0] == DIV:
                self.advance()
                result /= self.factor()
        return result

    def factor(self):
        if self.curr_token[0] == NUMBER:
            result = self.curr_token[1]
            self.advance()
            return result
        elif self.curr_token[0] == OPAREN:
            self.advance()
            result = self.expr()
            if self.curr_token[0] != CPAREN:
                raise ValueError("Expected closing parenthesis")
            self.advance()
            return result
        elif self.curr_token[0] == LOG:
            self.advance()
            if self.curr_token[0] != STRING:
                raise ValueError("Expected string after 'log'")
            print(self.curr_token[1])
            self.advance()
            return None
        else:
            raise ValueError(f"Unexpected token: {self.curr_token}")
lexer = Lexer(x)
tokens = lexer.tokenize()
parser = Parser(tokens)
result = parser.parse()
if result is not None:
    print(result)
