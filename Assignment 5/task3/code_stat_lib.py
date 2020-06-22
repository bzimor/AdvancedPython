from functools import wraps

from fpdf import FPDF
from PyPDF2 import PdfFileMerger, PdfFileReader

import inspect
import os
import sys, io
import fileinput
import math

import numpy as np
import matplotlib.pyplot as plt

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
def __get_operators__():
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

    result['N1'] = sum(result.values())
    return result


# checking the number of operands
def __get_operands__():
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

    n2['docstrings'] = docstrings
    n2['inlinedocs'] = inlinedocs

    numliterals = 0
    if literals:
        for v in literals.values():
            numliterals += v
    n2['literals'] = numliterals

    # anticipate if the value is 0
    if 'def' not in result:
        result['def'] = 0
    if 'assign' not in result:
        result['assign'] = 0

    n2['entities'] = result['def'] + result['assign']
    n2['args'] = 0
    n2['N2'] = sum(n2.values())
    return n2


# calculated and print halstead estimation
def __get_halstead__(N1, N2, x1, x2):
    vocabulary = x1 + x2
    length = N1 + N2
    # TODO: HARDCODED HERE
    calc_length = 17
    volume = length * math.log(vocabulary, 2)
    difficulty = ((x1 / 2) * (N2 / x2))
    effort = difficulty * volume

    result_halstead = dict()
    result_halstead['vocabulary'] = vocabulary
    result_halstead['volume'] = volume
    result_halstead['length'] = length
    result_halstead['calc_length'] = calc_length
    result_halstead['difficulty'] = difficulty
    result_halstead['effort'] = effort

    return result_halstead


# main function
def stat_complexity(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        source_code = inspect.getsource(func)
        lines = __filter_comments__(source_code)
        for line in lines:
            st_line = __filter_string__(line, "\"")
            st_line = __filter_string__(st_line, "\'")
            tokens = st_line.strip().split()
            for token in tokens:
                __filter_token__(token)

        complexity_result = dict()
        complexity_result['operators'] = __get_operators__()
        complexity_result['operands'] = __get_operands__()
        complexity_result['program'] = __get_halstead__(sum(n1.values()), sum(n2.values()), len(n1), len(n2))

        func.real_func = func
        func.complexity = complexity_result

        return func

    return wrapper


def stat_object(func):
    """Decorator for task 1, inspect the caller function using inspect.getsource()"""

    def get_doc(source):
        doc_str = ''
        if inspect.getdoc(source) != None:
            doc_str = inspect.getdoc(source)

        return doc_str

    def get_src(source):
        src_str = inspect.getsource(source)

        return src_str

    def print_result(result):
        print('{')
        for i in result:
            print('  {')
            for key, value in i.items():
                print('   ',key,' : ', value,',')
            print('  },')
        print('}')

    @wraps(func)
    def wrapper(*args, **kwargs):
        merged_result = calculate_object(func, *args, **kwargs)
        print_result(merged_result)

        # print_result(merged_result)

    return wrapper

def calculate_object(func, *args, **kwargs):
    def get_doc(source):
        doc_str = ''
        if inspect.getdoc(source) != None:
            doc_str = inspect.getdoc(source)

        return doc_str

    def get_src(source):
        src_str = inspect.getsource(source)

        return src_str

    result_stat_object = dict()

    # prev_result = func(*args, **kwargs)
    source = func 

    result_stat_object['Name'] = source.__name__
    result_stat_object['Type'] = type(source)
    result_stat_object['Sign'] = inspect.signature(source)
    result_stat_object['Args'] = source.__code__.co_varnames
    result_stat_object['Doc'] = get_doc(source)
    result_stat_object['Source'] = get_src(source)

    # Get Output here
    try:
        stdout = sys.stdout
        s = io.StringIO()
        sys.stdout = s
        source(*args, **kwargs)
        s.seek(0)
        sys.stdout = stdout
        output = s.read()
        output = output.splitlines()
        src_output = ''
        for i, o in enumerate(output):
            src_output += o
    except:
        src_output = ''

    result_stat_object['Output'] = src_output

    merged_result = [result_stat_object]

    return merged_result

def calculate_complexity(func, *args, **kwargs):
    source_code = inspect.getsource(func)
    lines = __filter_comments__(source_code)
    for line in lines:
        st_line = __filter_string__(line, "\"")
        st_line = __filter_string__(st_line, "\'")
        tokens = st_line.strip().split()
        for token in tokens:
            __filter_token__(token)

    complexity_result = dict()
    complexity_result['operators'] = __get_operators__()
    complexity_result['operands'] = __get_operands__()
    complexity_result['program'] = __get_halstead__(sum(n1.values()), sum(n2.values()), len(n1), len(n2))
    generate_plot(complexity_result)
    return complexity_result

def report_complexity(func):
    # canvas = Canvas("report_complexity.pdf", pagesize=LETTER)
    # t = canvas.beginText()
    # t.setFont('Helvetica', 10)
    # t.setCharSpace(4)
    # t.setTextOrigin(50, 600)

    @wraps(func)
    def wrapper(*args, **kwargs):
        merged_result = calculate_complexity(func, *args, **kwargs)
        result_str = ''
        for i in merged_result:
            result_str += '  {\n'
            result_str += i + ',\n'
            result_str += '  },\n'

        # t.textLines(result_str)
        # canvas.drawText(t)
        # canvas.showPage()
        # canvas.save()  
        return func
    return wrapper

def report_object(func):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)


    # canvas = Canvas("report_object.pdf", pagesize=LETTER)
    # t = canvas.beginText()
    # t.setFont('Helvetica', 10)
    # t.setCharSpace(3)
    # t.setTextOrigin(50, 700)

    @wraps(func)
    def wrapper(*args, **kwargs):
        merged_result = calculate_object(func, *args, **kwargs)
        result_str = ''
        index = 1
        # for i in merged_result:
        #     result_str += '  {\n'
        #     for key, value in i.items():
        #         result_str = '   '+str(key)+' : ' +str(value)+',\n'
        #         pdf.cell(200, 10, txt=result_str, ln=index, align="L")
        #         index += 1
        #     result_str = '  },\n'
        #     pdf.cell(200, 10, txt=result_str, ln=index, align="L")
        #     index += 1
        

        pdf.cell(200, 10, txt='{', ln=index, align="L")
        index += 1

        for i in merged_result:
            pdf.cell(200, 10, txt='  {', ln=index, align="L")
            index += 1
            for key, value in i.items():
                check_list = str(value).split('\n')
                if len(check_list) > 1:
                    for ix, t in enumerate(check_list):
                        if ix == 0:
                            pdf.cell(200, 10, txt='   ' + str(key) + ' : ' + str(t) + ',', ln=index, align="L")
                        else:
                            pdf.cell(200, 10, str(t) + ',', ln=index, align="L")                            
                        index += 1
                else:
                    pdf.cell(200, 10, txt='   ' + str(key) + ' : ' + str(value) + ',', ln=index, align="L")
                    index += 1

            pdf.cell(200, 10, txt='  },', ln=index, align="L")
            index += 1
        pdf.cell(200, 10, txt='},', ln=index, align="L")


        # pdf.cell(200, 10, txt=result_str, ln=1, align="L")
        # pdf.cell(200, 10, txt="Anjas", ln=2, align="L")
        
        pdf.output("report_object.pdf")

        # t.textLines(result_str)
        # canvas.drawText(t)
        # canvas.showPage()
        # # func(*args, **kwargs)
        # canvas.save()

    return wrapper


def generate_plot(final_result):
    if 'program' in final_result:
        indicators = tuple(final_result['program'].values())
            
        ind = np.arange(len(indicators))
        width = 0.35 

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, indicators, width,
                        color='Red', label='Indicators')
        ax.set_ylabel('Indicators')
        ax.set_title('Complexity of the code')
        ax.set_xticks(ind)
        ax.set_xticklabels(('Vocabulary', 'Length', 'Volume', 'Difficulty', 'Effort'))

        plt.savefig('report_complexity.pdf')

