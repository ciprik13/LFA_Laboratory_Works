import random
import re
from itertools import product

class CustomRegexParser:
    def __init__(self):
        self.superscript_map = {'²': 2, '³': 3}

    def parse(self, expression):
        result = ''
        i = 0
        while i < len(expression):
            char = expression[i]

            if i + 1 < len(expression) and expression[i + 1] in self.superscript_map:
                repeat = self.superscript_map[expression[i + 1]]
                result += char * repeat
                i += 2
            elif char == '(':
                end = expression.find(')', i)
                group = expression[i:end + 1]
                repeat = ''
                if end + 1 < len(expression) and expression[end + 1] in self.superscript_map:
                    repeat = '{' + str(self.superscript_map[expression[end + 1]]) + '}'
                    i = end + 2
                else:
                    i = end + 1
                result += group + repeat
            elif i + 1 < len(expression) and expression[i + 1] in '?*+':
                result += char + expression[i + 1]
                i += 2
            else:
                result += char
                i += 1
        return f'^{result}$'


class RegexInterpreter:
    def __init__(self):
        self.parser = CustomRegexParser()

    def interpret(self, string, expression):
        regex = self.parser.parse(expression)
        return re.match(regex, string) is not None


class Generator:
    def __init__(self):
        self.superscript_map = {'²': 2, '³': 3}

    def generate_regex(self, expression, count=10):
        samples = []
        for _ in range(count * 3):
            result = ''
            i = 0
            while i < len(expression):
                char = expression[i]

                if i + 1 < len(expression) and expression[i + 1] in '?*+':
                    q = expression[i + 1]
                    if q == '?':
                        result += random.choice([char, ''])
                    elif q == '*':
                        result += char * random.randint(0, 5)
                    elif q == '+':
                        result += char * random.randint(1, 5)
                    i += 2

                elif i + 1 < len(expression) and expression[i + 1] in self.superscript_map:
                    result += char * self.superscript_map[expression[i + 1]]
                    i += 2

                elif char == '(':
                    end = expression.find(')', i)
                    group_content = expression[i + 1:end]
                    options = group_content.split('|')
                    chosen = random.choice(options)
                    if end + 1 < len(expression) and expression[end + 1] in self.superscript_map:
                        repeat = self.superscript_map[expression[end + 1]]
                        result += ''.join(random.choices(options, k=repeat))
                        i = end + 2
                    else:
                        result += chosen
                        i = end + 1

                else:
                    result += char
                    i += 1

            samples.append(result)
        return list(set(samples))


regex_interpreter = RegexInterpreter()
generator = Generator()

def print_samples(expr, generator, interpreter):
    print(f"\n[Expression: {expr}]")
    print("Regex:", interpreter.parser.parse(expr))
    samples = generator.generate_regex(expr, count=10)
    for sample in samples[:10]:
        ok = interpreter.interpret(sample, expr)
        print(f"{sample} -> {'✔' if ok else '✘'}")

print_samples("A?B²(C|D)³E*F+", generator, regex_interpreter)
print_samples("(X|Y|Z)³8+(9|o)", generator, regex_interpreter)
print_samples("M?N²(0|P)³Q*R+", generator, regex_interpreter)
print_samples("(H|i)(J|K)L*N?", generator, regex_interpreter)
