# python -V 3.8

import fileinput
import math

operators = ['+', '-', '/', '*', '==', '!=', 'and', 'not', '=']
arithmetics = ['+', '-', '/', '*']
logics = ['==', '!=', 'and', 'not']
assign = ['=']
keywords = ['if', 'elif', 'else', 'try', 'for', 'with', 'return', 'def', 'import', 'except']

singleline_comment_op = "#"
multiline_comment_start_op = "'''"
multiline_comment_end_op = "'''"
n1 = {}
n2 = {}


def filter_token(token):
    tok = token
    while tok:
        tok = break_token(tok)


# parsing content inside string \" and \'
def filter_string(text, op):
    text = text.strip()
    occurrence = 0
    while op in text:
        s_start = text.find(op)
        if s_start != -1:
            s_end = text.find(op, s_start + 1)
        if s_start != -1 and s_end != -1:
            text = text.replace(text[s_start:s_end + 1], '')
        elif s_start != -1 and s_end == -1:
            occurrence += 1
            text = text.replace(op, 's' + str(occurrence))
        s_start = -1
        s_end = -1
    return text


# checking operator and keywords
def break_token(token):
    op_pos = len(token)
    for op in operators:
        if token.startswith(op):
            if op not in n1:
                n1[op] = 1
            else:
                n1[op] += 1
            return token[len(op):]
        if op in token:
            op_pos = min(op_pos, token.find(op))

    remaining_token = token[:op_pos]
    for keyword in keywords:
        if remaining_token == keyword:
            if keyword not in n1:
                n1[keyword] = 1
            else:
                n1[keyword] += 1

    if remaining_token not in n2:
        n2[remaining_token] = 1
    else:
        n2[remaining_token] += 1

    return token[op_pos:]


# checking comment string
def filter_comments(sourcecode_file):
    singleline_comment_op_pos = -1
    multiline_comment_start_op_pos = -1
    multiline_comment_end_op_pos = -1
    filtered_lines = []
    inside_comment = False
    for line in sourcecode_file:
        if not line.strip():
            continue
        if singleline_comment_op in line:
            singleline_comment_op_pos = line.find(singleline_comment_op)
        if multiline_comment_start_op in line:
            multiline_comment_start_op_pos = line.find(multiline_comment_start_op)
        if multiline_comment_end_op in line:
            multiline_comment_end_op_pos = line.find(multiline_comment_end_op)

        if (not inside_comment and singleline_comment_op_pos != -1):
            filtered_lines.append(line[:singleline_comment_op_pos])
        elif (inside_comment and multiline_comment_end_op_pos != -1):
            inside_comment = False
        elif (multiline_comment_start_op_pos != -1):
            inside_comment = True
        elif (inside_comment):
            inside_comment = True
        else:
            filtered_lines.append(line)
        singleline_comment_op_pos = -1
        multiline_comment_start_op_pos = -1
        multiline_comment_end_op_pos = -1

    return filtered_lines


# function to check the parenthesis in a string
def matched(str):
    match = False
    count = 0
    open_p = 0
    close_p = 0
    for i in str:
        if i == "(":
            open_p += 1
        elif i == ")":
            close_p += 1

    if open_p == close_p:
        match = True
        count = open_p
    else:
        match = False
        count = min(open_p, close_p)

    return match, count


# count calls by checking parenthesis
def count_calls():
    count = 0
    for n in n2:
        if n not in keywords:
            c = matched(n)
            count += c[1]

    return count


# Filter and print the result
def print_result():
    result = {}
    for key, value in n1.items():
        key_var = key
        if key in arithmetics:
            key_var = 'arithmetic'
        elif key in logics:
            key_var = 'logic'
        elif key in assign:
            key_var = 'assign'
        if key_var not in result:
            result[key_var] = 0
        result[key_var] += n1[key]

    # Only check the bracket, function name still be counted
    result['call'] = count_calls()

    # manually subtract 'function name' which is counted before in 'call'
    if 'def' in result:
        result['call'] -= result['def']

    print("[operators]")
    for key, value in result.items():
        print(key + ":", value)


def operands():
    docstring_start = False
    docstrings = 0
    inlinedocs = 0
    literals = {}
    singlequote = 0
    doublequote = 0
    for line in fileinput.input():
        inlinedoc_start = False
        singlequote_start = False
        doublequote_start = False
        templiteral = ''
        tempdigit = ''
        char_num = 1
        for char in line:
            if not inlinedoc_start and not singlequote_start and not doublequote_start:
                if char == "'":
                    singlequote = 1
                    doublequote = 0
                    singlequote_start = True
                    templiteral = ''
                    tempdigit = ''
                elif char == '"':
                    doublequote = 1
                    singlequote = 0
                    doublequote_start = True
                    templiteral = ''
                    tempdigit = ''
                elif char == "#":
                    inlinedocs += 1
                    inlinedoc_start = True
                    templiteral = ''
                    tempdigit = ''
                elif char.isnumeric():
                    tempdigit += char
                else:
                    if tempdigit:
                        if tempdigit not in literals.keys():
                            literals[tempdigit] = 0
                        literals[tempdigit] += 1
                    tempdigit = ''
            elif singlequote_start and not inlinedoc_start and not doublequote_start:
                if char == "'":
                    singlequote += 1
                    if singlequote == 3:
                        singlequote_start = False
                        if not docstring_start:
                            docstring_start = True
                            docstrings += 1
                        else:
                            docstring_start = False
                        singlequote = 0
                    elif singlequote == 2:
                        pass
                    else:
                        if templiteral not in literals.keys():
                            literals[templiteral] = 0
                        literals[templiteral] += 1
                        singlequote_start = False
                        templiteral = ''
                else:
                    singlequote = 0
                    templiteral += char
                    print(line)
                    print(templiteral)
            elif doublequote_start and not inlinedoc_start and not singlequote_start:
                if char == '"':
                    doublequote += 1
                    if doublequote == 3:
                        doublequote_start = False
                        if not docstring_start:
                            docstring_start = True
                            docstrings += 1
                        else:
                            docstring_start = False
                        doublequote = 0
                    elif doublequote == 2:
                        pass
                    else:
                        if templiteral not in literals.keys():
                            literals[templiteral] = 0
                        literals[templiteral] += 1
                        doublequote_start = False
                        templiteral = ''
                else:
                    doublequote = 0
                    templiteral += char
                    print(line)
                    print(templiteral)
            char_num += 1
            
    print('[operands]')
    n2['docstrings'] = docstrings
    n2['inlinedocs'] = inlinedocs
    print('docstrings: ' + str(docstrings))
    print('inlinedocs: ' + str(inlinedocs))
    numliterals = 0
    if literals:
        for v in literals.values():
            numliterals += v
    n2['literals'] = numliterals
    print("literals: " + str(numliterals))
    print(literals)


def print_halstead(N1, N2, n1, n2):
    vocabulary = n1 + n2
    length = N1 + N2
    calc_length = n1 * math.log(n1, 2) + n2 * math.log(n2, 2)
    volume = length * math.log(vocabulary, 2)
    difficulty = ((n1 / 2) * (N2 / n2))
    effort = difficulty * volume

    print('\n[program]')
    print('vocabulary: ', vocabulary)
    print('volume: ', volume)
    print('length: ', length)
    print('calc_length: ', calc_length)
    print('difficulty: ', difficulty)
    print('effort: ', effort)


# main function
def main():
    file = fileinput.input()
    lines = filter_comments(file)
    for line in lines:
        st_line = filter_string(line, "\"")
        st_line = filter_string(st_line, "\'")
        tokens = st_line.strip().split()
        for token in tokens:
            filter_token(token)

    print_result()
    operands()
    print_halstead(sum(n1.values()),sum(n2.values()),len(n1),len(n2))


if __name__ == "__main__":
    main()
