class Parser:
    '''
    use 'exit' to terminate the program
    '''
    def __init__(self):
        self.string = ''
        self.index = 0
        self.saved_result = []

    def set_value(self, string):
        self.string = string
        self.index = 0

    def getValue(self):
        value = self.parseExpression()
        self.skipWhitespace()
        if self.hasNext():
            raise Exception(
                "Unexpected character found: '" +
                self.peek() +
                "' at index " +
                str(self.index))

        self.saved_result.append(value)
        return len(self.saved_result) - 1, value

    def peek(self):
        return self.string[self.index:self.index + 1]

    def hasNext(self):
        return self.index < len(self.string)

    def skipWhitespace(self):
        while self.hasNext():
            if self.peek() in ' \t\n\r':
                self.index += 1
            else:
                return

    def parseExpression(self):
        return self.parseAddition()

    def parseAddition(self):
        values = [self.parseMultiplication()]
        while True:
            self.skipWhitespace()
            char = self.peek()
            if char == '+':
                self.index += 1
                values.append(self.parseMultiplication())
            elif char == '-':
                self.index += 1
                values.append(-1 * self.parseMultiplication())
            else:
                break

        result = 0
        for v in values:
            result += v
        return result

    def parseMultiplication(self):
        # TODO: Something here
        values = [self.parseParenthesis()]
        while True:
            self.skipWhitespace()
            char = self.peek()
            if char == '*':
                self.index += 1
                values.append(self.parseParenthesis())
            elif char == '/':
                div_index = self.index
                self.index += 1
                denominator = self.parseParenthesis()
                if denominator == 0:
                    raise Exception('error')
                values.append('/'+str(denominator))
            else:
                break
        value = 0
        first_val = 0
        for kkey, factor in enumerate(values):
            if kkey == 0:
                first_val = factor
                value = factor
            elif type(factor) is str:
                number_factor = int(factor[1:])
                check_value = value
                count = 0
                if number_factor < 0:
                    number_factor *= -1
                while check_value > 0:
                    check_value -= number_factor
                    if check_value >= 0:
                        count += 1
                value = count
            else:
                for i in range(factor-1):
                    value += first_val
                first_val = value

        return value

    def parseParenthesis(self):
        self.skipWhitespace()
        char = self.peek()
        if char == '(':
            self.index += 1
            value = self.parseExpression()
            self.skipWhitespace()
            if self.peek() != ')':
                raise Exception("err: invalid parenthesis")
            self.index += 1
            return value
        else:
            return self.parseNegative()

    def parseNegative(self):
        self.skipWhitespace()
        char = self.peek()
        if char == '-':
            self.index += 1
            return -1 * self.parseParenthesis()
        else:
            return self.parseValue()

    def parseValue(self):
        self.skipWhitespace()
        char = self.peek()
        if char in '0123456789.':
            return self.parseNumber()
        elif char == '[':
            return self.parseSavedValue()
        else:
            raise Exception('err: invalid number')

    def parseSavedValue(self):
        self.skipWhitespace()
        self.index += 1
        str_value = ''
        char = ''

        while self.hasNext():
            char = self.peek()
            if char == ']':
                self.index += 1
                break
            elif char in '0123456789':
                str_value += char
            else:
                raise Exception('err: invalid Exception')
            self.index += 1
        try:
            index_value = int(str_value)
        except:
            raise Exception('err: invalid index')

        return self.saved_result[index_value]

    def parseNumber(self):
        self.skipWhitespace()
        strValue = ''
        char = ''

        while self.hasNext():
            char = self.peek()
            if char == '.':
                raise Exception('invalid integer')
            elif char in '0123456789':
                strValue += char
            else:
                break
            self.index += 1

        if len(strValue) == 0:
            if char == '':
                raise Exception("err: invalid expression")
            else:
                raise Exception("err: invalid character")

        return int(strValue)


class check_pattern:
    def __init__(self, expression):
        self.expression = expression
        self.index = 0

    def peek(self, i):
        i += 1
        return self.expression[i:i + 1]

    def check(self):
        expect_close_bracket_1 = False
        expect_close_bracket_2 = False
        got_minus = False
        got_operator = False
        got_number = False

        for key, char in enumerate(self.expression):
            if char in '0123456789':
                if got_operator:
                    got_operator = False

                if got_number:
                    return False

                if key + 1 == len(self.expression):
                    pass
                elif self.peek(key) in '-+([':
                    return False
                elif self.peek(key) == ' ':
                    got_number = True
            elif char in '+*/':
                if got_operator:
                    return False

                if got_number:
                    got_number = False

                if self.peek(key) == ' ':
                    got_operator = True
                    pass
                else:
                    return False
            elif char == '-':
                got_minus = True

                if self.peek(key) in '0123456789':
                    if got_number:
                        return False
                    pass
                elif self.peek(key) == ' ':
                    if got_operator:
                        return False
                    got_operator = True
                    if got_number:
                        got_number = False
                    pass
                else:
                    return False

            elif char == '[':
                expect_close_bracket_1 = True
            elif char == ']':
                if not expect_close_bracket_1:
                    return False
                expect_close_bracket_1 = False
                if key + 1 == len(self.expression):
                    pass
                else:
                    if self.peek(key) == ' ':
                        pass
                    elif self.peek(key) == ')':
                        pass
                    else:
                        return False
            elif char == '(':
                if self.peek(key) in '-0123456789':
                    expect_close_bracket_2 = True
                    pass
                elif self.peek(key) == '[':
                    expect_close_bracket_2 = True
                    expect_close_bracket_1 = True
                    pass
                else:
                    return False

            elif char == ')':
                if not expect_close_bracket_2:
                    return False
                expect_close_bracket_2 = False
                if key + 1 == len(self.expression):
                    pass
                else:
                    if self.peek(key) == ' ':
                        pass
                    else:
                        return False
            elif char == ' ':
                got_minus = False
            else:
                if key == len(self.expression):
                    pass
                return False

        if expect_close_bracket_1 or expect_close_bracket_2:
            return False

        if expect_close_bracket_1 == False and expect_close_bracket_2 == False:
            return True


def main():
    arguments = sys.argv[1:]
    keep_looping = True

    if len(arguments) > 0 and arguments[0] == '-h':
        print(Parser.__doc__)
        keep_looping = False

    p = Parser()

    def evaluate(expression):
        correct_pattern = True
        checker = check_pattern(expression)
        correct_pattern = checker.check()
        if correct_pattern:
            try:
                p.set_value(expression)
                saved_key, value = p.getValue()
                print(saved_key, ': ', value)
            except Exception as ex:
                print('err: invalid expression')
        else:
            print('err: invalid expression')
            return None

    while keep_looping:
        try:
            command = input("\n>> ")
            if command == 'exit':
                keep_looping = False
            elif command != '':
                evaluate(command)
        except EOFError:
            keep_looping = False


main()
