# python -V 3.8

import sys
import fileinput

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
            
    print('[operands]')
    print('docstrings: ' + str(docstrings))
    print('inlinedocs: ' + str(inlinedocs))
    numliterals = 0
    if literals:
        for v in literals.values():
            numliterals += v
    print("literals: " + str(numliterals))

operands()