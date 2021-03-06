# python -V 3.8

import sys
import fileinput
import os

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
    N1_length = 0
    for key, value in result.items():
        print(key + ":", value)
        N1_length += value
    print("N1: " + str(N1_length))


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


if __name__ == "__main__":
    main()
