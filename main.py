import sympy as sp
from interpolation.lagrange import __lagrange_error_with_point

x = sp.Symbol('x')
my_function = sp.sin((sp.pi/6) * x)

print(sp.diff(my_function, x, 3))

print(my_function.subs(x, 1))

__lagrange_error_with_point(my_function, 2.5)

#solve_lagrange(my_function, (1, 2, 3))
