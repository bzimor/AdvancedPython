### Python Programming for Software Engineers
### Assignment 7
### 'Lambda De Parser'


# Team 7

# Task 1
# ----------------------------------------------
# Given the following:
f = lambda x, y: x * y


# 1. Rewrite to its logical equivalence using ordinary funcion definition(s)
# [code]
def f(x, y):
    return x * y


# Task 2
# ----------------------------------------------
# Given the following:
f = lambda x: (lambda y: (lambda z: x + y + z))
# 1. How would you call it to get the result of `x + y + z`?
# [code]
result = f(1)(2)(3)

# 2. Rewrite it using only one lambda expression and show how to call it
# [code]
f = lambda x, y, z: x + y + z

# how to call it
result = f(1, 2, 3)  # The parameter order refers to x, y, z
result = f(x=1, y=2, z=3)  # Specify the value for each parameter, order will not be matter
result = f(1, z=2, y=3)  # First value without specific parameter will read as an order (x)

# Task 3
# ----------------------------------------------
# Given the following:
(lambda b=(lambda *c: print(c)): b("a", "b"))()


# 1. What happens here? Rewrite it so that the code can be
# understood by a normal or your mate who has no idea what the lambda is!
# Provide comments, neat formatting and a bit more meaningful var names.
# [multiline code interlaced with comments]
def print_a_b():  # The function itself try to print a and b as a parameter
    def print_any_value(*value):  # define a function inside the first function to print any passed arguments
        print(value)  # print any given value

    print_any_value("a", "b")  # it calls another function which print any given arguments/parameters


print_a_b()  # call the function to print a and b

# ----------------------------------------------
# Task 4 (soft)
# ----------------------------------------------
# What are the main restrictions on the lambda?
# Provide "If yes, why? If not, why not?" for each of the following:
# 1. Does lambda restrict side effects?
# 2. Does lambda restrict number of allowed statements?
# 3. Does lambda restrict assignments?


# 4. Does lambda restrict number of return values?
# ANSWER:
# Lambda does not resrtrict the number of return value
# Basically when we return multiple return value we will use:
#       return a, b 
# It is equal with:
#       return (a, b)

# So we can do like this
custom_func = lambda a, b: (a, b)
# and use this to call
value_a, value_b = custom_func(17, "B")

# 5. Does lambda restrict the use of default arguments values?
# ANSWER:
# Lambda does not restrict the default arguments, here is an example:
custom_func = lambda a=5, b=10: a * b

# but it is also follows the rule that the default should be followed by another default arguments
# it is also applied to standard function
#       custom_func = lambda a = 5, b: a*b
# It will be throw an error because parameter b (has no default value) is written after a (which has default arguments)


# 6. Does lambda restrict possible function signatures?
# ANSWER:
# Lambda does not restrict the signature
# We can do like this
custom_func = lambda a, b: (a, b)
value_a, value_b = custom_func(b=10, a=2)
print("a:", value_a)
print("b:", value_b)
# We can pass the pass the arguments with the signature and the order won't be matter


# Task 5
# ----------------------------------------------
# Given the following:
(lambda f=(lambda a: (lambda b: print(list(map(lambda x: x + x, a + b))))):
 f((1, 2, 3))((4, 5, 6)))()

# 1. What happens here? Do the same as in Task 3 and
# enumerate order of execution using (1,2,3...) in comments
# [multiline code interlaced with comments]

# 2. Why does map() requires list() call?
# [written answer]
