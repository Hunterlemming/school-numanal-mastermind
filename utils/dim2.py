import sympy as sp

x = sp.Symbol('x')


def __convert_solution_to_list(solution):
    """
    Sometimes the sp.solve() ends up with some weird "OR" and "Equality" objects. I converted each of these to lists.

    :param solution: End-result of a sp.solve()
    :return: List of the solutions
    """
    if type(solution) == list:
        return solution
    result = []
    try:
        for equation in solution.args:
            # In case of "OR" objects, which separate equations
            result.append(int(equation.args[1]))
    except IndexError:
        # In case of a single equation
        result.append(int(solution.args[1]))
    return result


def __solve_equation(my_function, lower_limit=None, upper_limit=None):
    """
    Returns the possible x-values where the function equals 0.

    :param my_function: The function we are about to solve
    :param lower_limit: The lower x-limit of the interval
    :param upper_limit: The upper x-limit of the interval
    :return: A sp.solve() solution based on the parameters
    """
    if lower_limit is not None:
        if upper_limit is not None:
            return sp.solve([x >= lower_limit, x <= upper_limit, my_function], x)
        return sp.solve([x >= lower_limit, my_function], x)
    if upper_limit is not None:
        return sp.solve([x <= upper_limit, my_function], x)
    return sp.solve(my_function, x)


def get_minmax_info(my_function, lower_limit=None, upper_limit=None):
    """
    Calculates the possible minimum and maximum values of a function (in a given interval).

    :param my_function: The function in question (using Sympy symbol of x)
    :param lower_limit: [Optional] The lower x-limit of the interval
    :param upper_limit: [Optional] The upper x-limit of the interval
    :return: A dictionary of {
                x - Potential maximum/minimum location on the x axis,
                y - The function value in point x (maximum/minimum value),
                type - max || min || interval-limit || error (second derivative in point x is 0)
            }
    """
    minmax_info = []
    first_derivative = sp.diff(my_function)
    second_derivative = sp.diff(first_derivative)

    first_derivative_solution = __solve_equation(first_derivative, lower_limit, upper_limit)
    x_values_where_first_derivative_equals_zero = __convert_solution_to_list(first_derivative_solution)
    for x_value in x_values_where_first_derivative_equals_zero:
        y_value = second_derivative.subs(x, x_value)
        if y_value == 0:
            minmax_info.append({
                'x': x_value,
                'y': my_function.subs(x, x_value),
                'type': "error"})
        else:
            minmax_info.append({
                'x': x_value,
                'y': my_function.subs(x, x_value),
                'type': "max" if y_value < 0 else "min"
            })

    if lower_limit is not None:
        minmax_info.append({'x': lower_limit, 'y': my_function.subs(x, lower_limit), 'type': "interval-limit"})
    if upper_limit is not None:
        minmax_info.append({'x': upper_limit, 'y': my_function.subs(x, upper_limit), 'type': "interval-limit"})

    return minmax_info
