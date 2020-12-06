import sympy as sp
from interpolation.lagrange import __lagrange_error_with_point
from utils.dim2 import get_minmax_info


def convert_result_to_list(result):
    if type(result) == list:
        return result
    list_form = []
    for equation in result.args:
        list_form.append(int(equation.args[1]))
    return list_form


'''
x = sp.Symbol('x')
my_function = (x**4) - 2 * (x**2)
derived = sp.diff(my_function)
print(derived)
results = sp.solve([x >= -5, x <= 3, derived], x)
list_result = convert_result_to_list(results)
#results = sp.solve(derived)
print(list_result)
'''

x = sp.Symbol('x')
my_function = (x**4) - 2 * (x**2)
my_dict = get_minmax_info(my_function, lower_limit=-1.5, upper_limit=1.5)
print(my_dict)

'''
x = sp.Symbol('x')
my_function = sp.sin((sp.pi/6) * x)

print(sp.diff(my_function, x, 3))

print(my_function.subs(x, 1))

__lagrange_error_with_point(my_function, 2.5)
'''
#solve_lagrange(my_function, (1, 2, 3))
