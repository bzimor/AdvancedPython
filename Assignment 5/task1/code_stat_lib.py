import inspect
import os
import sys, io
import fileinput
import math

operators = ['+', '-', '/', '*', '==', '!=', 'and', 'not', '=']
arithmetics = ['+', '-', '/', '*']
logics = ['==', '!=', 'and', 'not']
assign = ['=']
keywords = ['if', 'elif', 'else', 'try', 'for', 'with', 'return', 'def', 'import', 'except']

filelines = []
singleline_comment_op = "#"
multiline_comment_start_op = "'''"
multiline_comment_end_op = "'''"
n1 = {}
n2 = {}
result = {}


def stat_object(func):
    """Decorator for task 1, inspect the caller function using inspect.getsource()"""

    def get_doc():
        doc_str = ''
        if inspect.getdoc(func) != None:
            doc_list = inspect.getdoc(func).split("\n")
            for (i, value) in enumerate(doc_list):
                header = ''
                if i == 0: header = 'Doc:'
                doc_str += '{:9}{}'.format(header, value + "\n")
        else:
            doc_str = '{:9}'.format('Doc:')
        return doc_str

    def get_src():
        src_list = inspect.getsource(func).split("\n")
        src_str = ''
        for (i, value) in enumerate(src_list):
            header = ''
            if i == 0: header = 'Source:'
            src_str += '{:9}{}'.format(header, value + "\n")
        return src_str

    def get_complx():
        words = ['print', 'for', 'if']
        result = dict()
        for x in words:
            c_words = inspect.getsource(func).count(x)
            if c_words > 0:
                result[x] = c_words
        return '{:9}{}'.format('Complx:', str(result))

    def func_wrapper(*args, **kwargs):
        print('{:9}{}'.format('Name:', func.__name__))
        print('{:9}{}'.format('Type:', type(func)))
        print('{:9}{}'.format('Sign:', inspect.signature(func)))
        print('{:9}{}'.format('Args:', func.__code__.co_varnames))
        print(get_doc())
        print(get_src())
        try:
            stdout = sys.stdout
            s = io.StringIO()
            sys.stdout = s
            func(*args, **kwargs)
            s.seek(0)
            sys.stdout = stdout
            output = s.read()
            output = output.splitlines()
            for i, o in enumerate(output):
                if i == 0:
                    print('{:9}{}'.format('Output:', o))
                else:
                    print('{:9}{}'.format('', o))

        except:
            print("Output:")

    return func_wrapper


def __filter_token__(token):
    tok = token
    while tok:
        tok = __break_token__(tok)


# parsing content inside string \" and \'
def __filter_string__(text, op):
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
def __break_token__(token):
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

    return token[op_pos:]


# checking comment string
def __filter_comments__(sourcecode_file):
    global filelines
    singleline_comment_op_pos = -1
    multiline_comment_start_op_pos = -1
    multiline_comment_end_op_pos = -1
    filtered_lines = []
    inside_comment = False
    for line in sourcecode_file:
        filelines.append(line)
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
def __matched__(str):
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
def __count_calls__():
    count = 0
    for n in n2:
        if n not in keywords:
            c = __matched__(n)
            count += c[1]

    return count


# Filter and print the result
def __print_result__():
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
    result['calls'] = __count_calls__()

    # manually subtract 'function name' which is counted before in 'call'
    if 'def' in result and result['calls']:
        result['calls'] -= result['def']

    print("[operators]")
    for key, value in result.items():
        print(key + ":", value)
    print("N1: " + str(sum(result.values())))


# checking the number of operands
def __operands__():
    global filelines
    docstring_start = False
    docstrings = 0
    inlinedocs = 0
    literals = {}
    singlequote = 0
    doublequote = 0
    for line in filelines:
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
            char_num += 1

    print('\n[operands]')
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

    # anticipate if the value is 0
    if 'def' not in result:
        result['def'] = 0
    if 'assign' not in result:
        result['assign'] = 0

    n2['entities'] = result['def'] + result['assign']
    print("entities: " + str(n2['entities']))
    print("args: calculating... wait")
    print("N2: " + str(sum(n2.values())))


# calculated and print halstead estimation
def __print_halstead__(N1, N2, n1, n2):
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
def stat_complexity(func):
    def func_wrapper(*args, **kwargs):
        try:
            source_code = inspect.getsource(func)
            lines = __filter_comments__(source_code)
            for line in lines:
                st_line = __filter_string__(line, "\"")
                st_line = __filter_string__(st_line, "\'")
                tokens = st_line.strip().split()
                for token in tokens:
                    __filter_token__(token)

            __print_result__()
            __operands__()
            __print_halstead__(sum(n1.values()), sum(n2.values()), len(n1), len(n2))
        except:
            print("Output:")

    return func_wrapper
