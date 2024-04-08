from pysat.solvers import Glucose3
import math


def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]


def binary_encoding(clauses, target, new_variables):
    for i in range(len(new_variables)):
        clauses.append([-target, new_variables[i]])


def generate_binary_combinations(n):
    binary_combinations = []
    for i in range(1 << n):
        binary_combinations.append(format(i, '0' + str(n) + 'b'))
    return binary_combinations

def generate_new_variables(end, length):
    return [i for i in range(end + 1, end + math.ceil(math.log(length, 2)) + 1)]


def at_most_one(clauses, new_variables, variables):
    temp_new_variables = generate_new_variables(n ** 2 + len(new_variables), len(variables))
    new_variables += temp_new_variables
    binary_combinations = generate_binary_combinations(len(temp_new_variables))

    for i in range(len(variables)):
        combination = binary_combinations[i]
        temp_clause = []
        for j in range(len(combination) - 1, -1, -1):
            index = len(combination) - j - 1
            temp_clause.append({True: temp_new_variables[index], False: -temp_new_variables[index]} [int(combination[j]) == 1])

        binary_encoding(clauses, variables[i], temp_clause)


def exactly_one(clauses, new_variables, variables):
    clauses.append(variables)
    at_most_one(clauses, new_variables, variables)


def generate_clauses(n, variables):
    clauses = []
    new_variables = []

    # Exactly one queen in each row
    for i in range(n):
        exactly_one(clauses, new_variables, variables[i])

    # Exactly one queen in each column
    for j in range(n):
        exactly_one(clauses, new_variables, [variables[i][j] for i in range(n)])


    # At most one queen in each diagonal
    for i in range(1, n):
        diagonal = []
        row = i
        col = 0
        while row >= 0 and col < n:
            diagonal.append(variables[row][col])
            row -= 1
            col += 1
        at_most_one(clauses, new_variables, diagonal)

    for j in range(1, n - 1):
        diagonal = []
        row = n - 1
        col = j
        while row >= 0 and col < n:
            diagonal.append(variables[row][col])
            row -= 1
            col += 1
        at_most_one(clauses, new_variables, diagonal)

    for i in range(n - 1):
        diagonal = []
        row = i
        col = 0
        while row < n and col < n:
            diagonal.append(variables[row][col])
            row += 1
            col += 1
        at_most_one(clauses, new_variables, diagonal)

    for j in range(1, n - 1):
        diagonal = []
        row = 0
        col = j
        while row < n and col < n:
            diagonal.append(variables[row][col])
            row += 1
            col += 1
        at_most_one(clauses, new_variables, diagonal)

    return clauses


def solve_n_queens(n):
    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
    else:
        return None


def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


n = 8
solution = solve_n_queens(n)
print_solution(solution)

