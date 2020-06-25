history = []

class Fraction:
    val1 = 0
    val2 = 0

    def expand(self, val):
        v = val.split('/')
        return str(int(v[0])/int(v[1]))


    def parse(self, exp):
        values = exp.split()
        if len(values) == 1:
            return exp
        if values[0].isnumeric() and values[2].isnumeric():
            if values[1] == '/':
                return str(int(values[0])/int(values[2]))

        self.val1 = values[0].split('/')
        self.val2 = values[2].split('/')
        if values[1] == '+':
            return self.__add__()
        elif values[1] == '/':
            return self.__div__()

    def __add__(self):
        den = 0
        for i in range(int(self.val2[1])):
            den += int(self.val1[1])

        num1 = 0
        num2 = 0
        for i in range(int(self.val2[1])):
            num1 += int(self.val1[0])
        for i in range(int(self.val1[1])):
            num2 += int(self.val2[0])

        return str(num1+num2) + '/' + str(den)

    def __div__(self):
        return str(self.val2[1]) + '/' + str(self.val1[1])


def main():
    keep_looping = True
    def evaluate(expression):
        global history
        try:
            fr = Fraction()
            result = ''
            val = 0
            if expression.startswith('expand '):
                if expression.endswith(']'):
                    k = expression.replace('expand ', '').replace('[', '').replace(']', '')
                    if k.isnumeric() and len(history) > int(k):
                        val = history[int(k)]
                else:
                    val = expression.replace('expand ', '')
                result = fr.expand(val)
            else:
                result = fr.parse(expression)
            history.append(result)
            print(str(len(history)-1), ': ', result)
        except Exception as ex:
            print('err: invalid expression')
    

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
