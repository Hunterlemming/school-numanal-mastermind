import sympy as sp
import math
from utils.dim2 import get_global_abs_max

x = sp.Symbol('x')
n = 0


def __lagrange(function_to_evaluate, starting_points):
    global n
    number_of_starting_points = len(starting_points)
    n = number_of_starting_points - 1
    lagrange_polynomial = {}

    for i in range(number_of_starting_points):
        dividend = []
        divisor = []
        for j in range(number_of_starting_points):
            if i != j:
                if 0 <= starting_points[j]:
                    dividend.append(f"(x - {starting_points[j]})")
                    divisor.append(f"({starting_points[i]} - {starting_points[j]})")
                else:
                    dividend.append(f"(x + {abs(starting_points[j])})")
                    divisor.append(f"({starting_points[i]} + {abs(starting_points[j])})")
        lagrange_polynomial[f'l{i}'] = "".join(dividend) + "/" + "".join(divisor)

        evaluation_at_current_starting_point = function_to_evaluate.subs(x, starting_points[i])
        if "full" not in lagrange_polynomial:
            lagrange_polynomial["full"] = []
            lagrange_polynomial["full"].append(f"({evaluation_at_current_starting_point}) * "
                                               + f"({lagrange_polynomial[f'l{i}']})")
        else:
            lagrange_polynomial["full"].append(" + ")
            lagrange_polynomial["full"].append(f"({evaluation_at_current_starting_point}) * "
                                               + f"({lagrange_polynomial[f'l{i}']})")
    lagrange_polynomial["full"] = "".join(lagrange_polynomial["full"])

    return lagrange_polynomial


def __lagrange_error(function_to_evaluate, starting_points, error_info):
    if n == 0 or error_info is None:
        return None
    else:
        error_evaluation = {'nth-derivative': sp.diff(function_to_evaluate, x, n + 1)}
        error_evaluation['M'] = get_global_abs_max(error_evaluation['nth-derivative'],
                                                   error_info['interval-lower-limit'],
                                                   error_info['interval-upper-limit']).get("y")
        if 'point' in error_info:
            diff_to_starting_vector = 1
            for element in starting_points:
                diff_to_starting_vector *= (error_info['point'] - element)
            error_evaluation['result'] = error_evaluation['M'] * abs(diff_to_starting_vector) / math.factorial(n+1)
        if 'err_interval' in error_info:
            diff_to_interval = ((error_info['err_interval']['end'] - error_info['err_interval']['start']) / n) ** (n+1)
            error_evaluation['result'] = error_evaluation['M'] * diff_to_interval / (4 * (n+1))
        return error_evaluation


def solve_lagrange(function_to_evaluate, starting_points, error_info=None):
    inter_result = __lagrange(function_to_evaluate, starting_points)
    print("\n< LAGRANGE >")
    print("\n_________________")
    print("Iteration result:\n")
    for key in inter_result:
        if key.startswith("l"):
            print(f"{key}(x):  {inter_result.get(key)}")
    print(f"\nL{n}(x):  {inter_result['full']}")

    error_result = __lagrange_error(function_to_evaluate, starting_points, error_info)
    if error_result is not None:
        print("\n_________________")
        print("Error estimation:\n")
        print(f"n: {n} => {n+1}. derivative: {error_result['nth-derivative']}")
        print(f"M{n+1}: {error_result['M']}\n")

        if 'point' in error_info:
            print(f"|f(x) - L{n}(x)|  <=  M{n}+1 * |(x - x0) * ... * (x - x{n})| / ({n}+1)!")
            substitution = []
            for current_x_value in starting_points:
                if len(substitution) > 0:
                    substitution.append(" * ")
                substitution.append(f"({error_info['point']} - {current_x_value})")
            print(f"|f(x) - L{n}(x)|  <=  ({error_result['M']}) * |{''.join(substitution)}| / {n + 1}!")
            print(f"|f(x) - L{n}(x)|  <=  {error_result['result']}")

        if 'err_interval' in error_info:
            print(f"|f(x) - L{n}(x)|  <=  M{n}+1 * ((b - a) / {n})^({n}+1) / (4 * ({n}+1))")
            print(f"|f(x) - L{n}(x)|  <=  ({error_result['M']}) * "
                  f"(({error_info['err_interval']['end']} - {error_info['err_interval']['start']}) / {n})^{n+1} / "
                  f"(4 * ({n+1}))")
            print(f"|f(x) - L{n}(x)|  <=  {error_result['result']}")
