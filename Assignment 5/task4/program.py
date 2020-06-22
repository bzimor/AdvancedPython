from code_stat_lib import *

rc(multipage=True, filename='report.pdf', papersize='a4')

@report_object
@report_complexity

def foo(z, x):
    '''
    another dummy comment
    '''
    # this is comment
    print('what are you looking for?')


if __name__ == "__main__":
    foo('args', 2)
