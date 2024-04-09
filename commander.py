import math

from pysat.solvers import Glucose3

new_variables_count = 0
def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]


def generate_new_variables(start, length):
    return [i for i in range(start, start + length)]


def grouping_variables(variables, per_group):
    groups = []
    temp_groups = []
    for i in range(len(variables)):
        temp_groups.append(variables[i])
        if((i + 1) % per_group == 0 or i == len(variables) - 1):
            groups.append(temp_groups)
            temp_groups = []
    return groups

def generate_commanders(start, length):
    return [i for i in range(start, start + length)]


def binomial_AMO(clauses, variables):
    for i in range(0, len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])
    return clauses


def binomial_EO(clauses, variables):
    clauses.append(variables)
    binomial_AMO(clauses, variables)



def at_most_one(clauses, variables):
        global new_variables_count
        groups = grouping_variables(variables, n/math.floor(math.sqrt(n)))
        commanders = generate_commanders(n ** 2 + new_variables_count + 1, len(groups))
        new_variables_count += len(groups)
        binomial_AMO(clauses, commanders)

        for i in range(len(commanders)):
            binomial_AMO(clauses, groups[i])
            clauses.append(groups[i] + [-commanders[i]])
            for j in range(len(groups[i])):
                clauses.append([commanders[i], -groups[i][j]])

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
        print("before call amo")
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
    print(clauses)

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