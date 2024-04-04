from pysat.solvers import Glucose3


def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]


def generate_clauses(n, variables):
    clauses = []

    # Exactly one queen in each row
    for i in range(n):
        clauses.append(variables[i])
        for j in range(n):
            for k in range(j + 1, n):
                clauses.append([-variables[i][j], -variables[i][k]])

    # Exactly one queen in each column
    for j in range(n):
        clauses.append([variables[i][j] for i in range(n)])
        for i in range(n):
            for k in range(i + 1, n):
                clauses.append([-variables[i][j], -variables[k][j]])

    # At most one queen in each diagonal
    for i in range(n):
        for j in range(n):
            for k in range(1, n):
                if i + k < n and j + k < n:
                    clauses.append([-variables[i][j], -variables[i + k][j + k]])
                if i + k < n and j - k >= 0:
                    clauses.append([-variables[i][j], -variables[i + k][j - k]])

    return clauses


def solve_n_queens(n):
    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        print(model)
        return [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
    else:
        return None


def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


n = 11
solution = solve_n_queens(n)
print_solution(solution)