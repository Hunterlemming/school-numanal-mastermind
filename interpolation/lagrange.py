import sympy as sp

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
                    divisor.append(f"({starting_points[i]} - {abs(starting_points[j])})")
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


def __lagrange_error_with_point(function_to_evaluate, point):
    pass


def solve_lagrange(function_to_evaluate, starting_points, error=None):
    inter_result = __lagrange(function_to_evaluate, starting_points)
    print("Iteration result:\n")
    for key in inter_result:
        if key.startswith("l"):
            print(f"{key}(x):  {inter_result.get(key)}")
    print(f"\nL(x):  {inter_result['full']}")
