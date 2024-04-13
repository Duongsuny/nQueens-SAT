import product

board_sizes = [4, 8, 16, 32, 64, 128, 256, 512]

for n in board_sizes:
    product.solve_n_queens(n)