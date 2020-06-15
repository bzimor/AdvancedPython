import inspect
import os
import inspect


def reflect(func):
    """Decorator for task 1, inspect the caller function using inspect.getsource()"""

    def get_doc():
        doc_list = inspect.getdoc(func).split("\n")
        doc_str = ''
        for (i, value) in enumerate(doc_list):
            header = ''
            if i == 0: header = 'Doc:'
            doc_str += '{:9}{}'.format(header, value + "\n")
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
        print(get_complx())
        print(get_src())
        print('{:9}'.format('Output:', ''))
        try:
            func(*args, **kwargs)
        except:
            print("No text output")

    return func_wrapper


@reflect
def foo(bar1, bar2=""):
    """
    This function does nothing useful
    :param bar1: description
    :param bar2: description
    """
    print("some\nmultiline\noutput")


if __name__ == "__main__":
    foo(None, "ss")
    test = reflect
    baar = reflect(test)
    baar()