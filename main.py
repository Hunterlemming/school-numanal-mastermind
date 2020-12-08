import sympy as sp
import math
from interpolation.lagrange import __lagrange_error, solve_lagrange
from utils.dim2 import get_minmax_info, get_global_max, get_global_abs_max


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

'''
x = sp.Symbol('x')
my_function = (x**4) - 2 * (x**2)
my_dict = get_minmax_info(my_function, lower_limit=-1.5, upper_limit=1.5)
print(my_dict)
print(get_global_max(my_function))
'''


x = sp.Symbol('x')
#my_function = sp.sin((sp.pi/6) * x)
my_function = (x**4) - 2 * (x**2)
'''
third_derivative = sp.diff(my_function, x, 3)
print(third_derivative)

print(f"max:  {get_global_max(third_derivative, lower_limit=1, upper_limit=3)}")
print(f"abs-max: {get_global_abs_max(third_derivative, lower_limit=1, upper_limit=3)}")

print(my_function.subs(x, 1))

__lagrange_error(my_function, 2.5, )
'''

solve_lagrange(my_function, (-math.sqrt(2), -1, 0, 1, math.sqrt(2)), {
    'interval-lower-limit': -2,
    'interval-upper-limit': 2,
    'point': 2.5
})

solve_lagrange(my_function, (-1, 0, 1), {
    'interval-lower-limit': -1,
    'interval-upper-limit': 1,
    'err_interval': {'start': -1, 'end': 1}
})
