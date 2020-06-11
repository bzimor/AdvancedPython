import inspect


def reflect(func):
    """Decorator for task 1, inspect the caller function using inspect.getsource()"""
    def func_wrapper():
        print(inspect.getsource(func))

    return func_wrapper


@reflect
def foo():
    print("bar")


if __name__ == "__main__":
    foo()
