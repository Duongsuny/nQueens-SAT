import math
from pysat.solvers import Glucose3
import time

start_time = time.time()
new_variables_count = 0

def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]


def binomial_AMO(clauses, variables):
    for i in range(0, len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])
    return clauses

def generate_matrix(start, variables_length):
    p = math.ceil(math.sqrt(variables_length))
    q = math.ceil(n / p)
    return [
        [i for i in range(start, start + p)],
        [j for j in range(start + p, start + p + q)]
    ]


def generate_binary_combinations(n):
    binary_combinations = []
    for i in range(1 << n):
        binary_combinations.append(format(i, '0' + str(n) + 'b'))
    return binary_combinations


def binary_encoding(clauses, target, new_variables):
    for i in range(len(new_variables)):
        clauses.append([-target, new_variables[i]])

def generate_new_variables(end, length):
    return [i for i in range(end + 1, end + math.ceil(math.log(length, 2)) + 1)]

def binary_AMO(clauses, variables):
    global new_variables_count
    temp_new_variables = generate_new_variables(n ** 2 + new_variables_count, len(variables))
    new_variables_count += len(temp_new_variables)
    binary_combinations = generate_binary_combinations(len(temp_new_variables))

    for i in range(len(variables)):
        combination = binary_combinations[i]
        temp_clause = []
        for j in range(len(combination) - 1, -1, -1):
            index = len(combination) - j - 1
            temp_clause.append({True: temp_new_variables[index], False: -temp_new_variables[index]} [int(combination[j]) == 1])

        binary_encoding(clauses, variables[i], temp_clause)

def at_most_one(clauses, variables):
    global new_variables_count
    matrix = generate_matrix(n ** 2 + new_variables_count + 1, len(variables))
    row = matrix[0]
    col = matrix[1]
    new_variables_count += len(row) + len(col)

    if(len(variables) > 10):
        binary_AMO(clauses, row)
        binary_AMO(clauses, col)
    else:
        binomial_AMO(clauses, row)
        binomial_AMO(clauses, col)

    x = 0
    for i in range(len(row)):
        for j in range(len(col)):
            clauses.append([-variables[x], row[i]])
            clauses.append([-variables[x], col[j]])
            x += 1
            if x == len(variables): break
        if x == len(variables): break

def exactly_one(clauses, variables):
    clauses.append(variables)
    at_most_one(clauses, variables)

def generate_clauses(n, variables):
    clauses = []

    # Exactly one queen in each row
    for row in range(n):
        exactly_one(clauses, variables[row])

    # Exactly one queen in each column
    for col in range(n):
        exactly_one(clauses, [variables[row][col] for row in range(n)])

    # At most one queen in each diagonal
    for i in range(1, n):
        diagonal = []
        row = i
        col = 0
        while row >= 0 and col < n:
            diagonal.append(variables[row][col])
            row -= 1
            col += 1
        at_most_one(clauses, diagonal)

    for j in range(1, n - 1):
        diagonal = []
        row = n - 1
        col = j
        while row >= 0 and col < n:
            diagonal.append(variables[row][col])
            row -= 1
            col += 1
        at_most_one(clauses, diagonal)

    for i in range(n - 1):
        diagonal = []
        row = i
        col = 0
        while row < n and col < n:
            diagonal.append(variables[row][col])
            row += 1
            col += 1
        at_most_one(clauses, diagonal)

    for j in range(1, n - 1):
        diagonal = []
        row = 0
        col = j
        while row < n and col < n:
            diagonal.append(variables[row][col])
            row += 1
            col += 1
        at_most_one(clauses, diagonal)

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


n = 128
solution = solve_n_queens(n)
print_solution(solution)
print("Run time:  %s seconds" % (time.time() - start_time))