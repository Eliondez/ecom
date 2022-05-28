from random import randint, random
print('Matrix inverter')


class Inverter:
    def __init__(self):
        self.size = 10
        self.matrix = []
        for row in range(self.size):
            row = [0] * self.size
            self.matrix.append(row)

    def invert(self, row_num=-1, col_num=-1):
        if row_num > -1:
            for col in range(self.size):
                print(row_num, col)
                self.matrix[row_num][col] = int(not bool(self.matrix[row_num][col]))
        if col_num > -1:
            for row in range(self.size):
                self.matrix[row][col_num] = int(not bool(self.matrix[row][col_num]))

    def invert_row(self, n):
        self.invert(n, -1)

    def invert_col(self, n):
        self.invert(-1, n)


    def print_matrix(self):
        for row in self.matrix:
            print(row)
        print()

c = Inverter()
row_inverts = 0
col_inverts = 0

for i in range(150):
    if random() > 0.7:
        c.invert_row(randint(0, 9))
        row_inverts += 1
    if random() > 0.7:
        c.invert_col(randint(0, 9))
        col_inverts += 1

# print('row_inverts', row_inverts)
# print('col_inverts', col_inverts)

c.print_matrix()

