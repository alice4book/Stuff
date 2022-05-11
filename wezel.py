

def swap_in_matrix(m, i, j, op, operator, M, N):
    o_m = []
    new_zero = []
    for k in m:
        o_m.append(k.copy())

    if op == 'L':
        o_m[i][j], o_m[i][j-1] = o_m[i][j-1], o_m[i][j]
        new_zero = [i, j-1]
    if op == 'R':
        o_m[i][j], o_m[i][j+1] = o_m[i][j+1], o_m[i][j]
        new_zero = [i, j+1]
    if op == 'U':
        o_m[i][j], o_m[i-1][j] = o_m[i-1][j], o_m[i][j]
        new_zero = [i-1, j]
    if op == 'D':
        o_m[i][j], o_m[i+1][j] = o_m[i+1][j], o_m[i][j]
        new_zero = [i+1, j]
    return Wezel(o_m, new_zero, operator, M, N)


class Wezel(object):
    def __init__(self, matrix, zero, operators, M, N):
        self.matrix = matrix
        self.zero = zero
        self.operators = operators
        self.priority = 0
        self.deep = 0
        self.M = M
        self.N = N
        matrix_str = ""
        for i in range(self.M):
            for j in range(self.N):
                matrix_str += str(matrix[i][j])
        self.hash_value = hash(matrix_str)


    def get_zero(self):
        return self.zero

    def get_hash(self):
        return self.hash_value

    def set_deep(self, add):
        self.deep = add + 1

    def get_deep(self):
        return self.deep

    def __lt__(self, point_ov):
        return self.priority < point_ov.priority

    def set_priority(self, priority):
        self.priority = priority

    def get_priority(self):
        return self.priority

    def get_matrix(self):
        return self.matrix

    def get_operators(self):
        return self.operators

    def isGoal(self, s):
        return self.get_hash() == s.get_hash()

    def neighbours(self, op):
        i = self.zero[0]
        j = self.zero[1]
        tab = []
        for k in op:
            if k == 'L':
                if j-1 < 0:
                    tab.append('-')
                else:
                    tab.append(swap_in_matrix(self.matrix, i, j, 'L', self.operators+"L", self.M, self.N))
            if k == 'R':
                if j+1 >= self.N:
                    tab.append('-')
                else:
                    tab.append(swap_in_matrix(self.matrix, i, j, 'R', self.operators+"R", self.M, self.N))
            if k == 'U':
                if i-1 < 0:
                    tab.append('-')
                else:
                    tab.append(swap_in_matrix(self.matrix, i, j, 'U', self.operators+"U", self.M, self.N))
            if k == 'D':
                if i+1 >= self.M:
                    tab.append('-')
                else:
                    tab.append(swap_in_matrix(self.matrix, i, j, 'D', self.operators+"D", self.M, self.N))
        return tab
