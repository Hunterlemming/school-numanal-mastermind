import sympy as sp

x = sp.Symbol('x')


def __solve_equations_in_or(sympy_or_object):
    result = []
    equations_in_or = [element for element in sympy_or_object.args if isinstance(element, sp.Eq)]
    for equation in equations_in_or:
        for element in sp.solve(equation):
            result.append(element)
    return result


def __solve_equations_in_and(sympy_and_object):
    result = []
    interval_conditions = [elm for elm in sympy_and_object.args if isinstance(elm, sp.LessThan)]
    or_object_containing_equations = [element for element in sympy_and_object.args if isinstance(element, sp.Or)][0]
    or_results = __solve_equations_in_or(or_object_containing_equations)
    for possible_result in or_results:
        valid = True
        for condition in interval_conditions:
            if not bool(condition.subs(x, possible_result)):
                valid = False
        if valid:
            result.append(possible_result)
    return result


def __convert_solution_to_list(solution):
    """
    Sometimes the sp.solve() ends up with "AND", "OR" and "Equality" objects. I converted each of these to lists.

    :param solution: End-result of a sp.solve()
    :return: List of the solutions
    """
    if type(solution) == list:
        return solution
    if isinstance(solution, sp.Eq):
        return sp.solve(solution)
    if isinstance(solution, sp.Or):
        return __solve_equations_in_or(solution)
    if isinstance(solution, sp.And):
        return __solve_equations_in_and(solution)


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
                type - max || min || interval-limit
            }
    """
    minmax_info = []
    first_derivative = sp.diff(my_function)
    second_derivative = sp.diff(first_derivative)

    if second_derivative != 0:
        first_derivative_solution = __solve_equation(first_derivative, lower_limit, upper_limit)
        x_values_where_first_derivative_equals_zero = __convert_solution_to_list(first_derivative_solution)
        for x_value in x_values_where_first_derivative_equals_zero:
            y_value = second_derivative.subs(x, x_value)
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


def get_global_max(my_function, lower_limit=None, upper_limit=None, _abs=False):
    minmax_info = get_minmax_info(my_function, lower_limit, upper_limit)
    global_max = None
    max_value = None
    for element in minmax_info:
        current_y_value = abs(element['y']) if _abs else element['y']
        if max_value is None or max_value < current_y_value:
            max_value = current_y_value
            global_max = element
            global_max['y'] = current_y_value
    return global_max


def get_global_abs_max(my_function, lower_limit=None, upper_limit=None):
    return get_global_max(my_function, lower_limit=lower_limit, upper_limit=upper_limit, _abs=True)
