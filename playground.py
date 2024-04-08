def print_diagonals(board):
    n = len(board)
    for i in range(1, n):
        diagonal = []
        row = i
        col = 0
        while row >= 0 and col < n:
            diagonal.append(board[row][col])
            row -= 1
            col += 1
        print(diagonal)

    for j in range(1, n - 1):
        diagonal = []
        row = n - 1
        col = j
        while row >= 0 and col < n:
            diagonal.append(board[row][col])
            row -= 1
            col += 1
        print(diagonal)

    for i in range(n - 1):
        diagonal = []
        row = i
        col = 0
        while row < n and col < n:
            diagonal.append(board[row][col])
            row += 1
            col += 1
        print(diagonal)

    for j in range(1, n - 1):
        diagonal = []
        row = 0
        col = j
        while row < n and col < n:
            diagonal.append(board[row][col])
            row += 1
            col += 1
        print(diagonal)

# Example usage
board = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]
print_diagonals(board)
