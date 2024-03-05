import numpy as np

def manager(c, A, b, A_signs, min_max, x_signs):
    M1, M2, N1, N2 = [], [], [], []

    for i in range(len(A_signs)):
        if A_signs[i] == '<=':
            A_signs[i] = '>='
            for j in range(len(A[i])):
                A[i][j] *= -1
            for k in range(len(b)):
                if k == i:
                    b[k] *= -1
        if A_signs[i] == '>=':
            M1.append(i)
        if A_signs[i] == '=':
            M2.append(i)
    for i in range(len(b)):
        if i in x_signs:
            N1.append(i)
        else:
            N2.append(i)

    if min_max == 'max':
        min_max_new = 'min'
        for i in range(len(c)):
            c[i] *= -1
    else:
        min_max_new = 'min'

    return M1, M2, N1, N2, min_max_new

def common_to_canonical(c, A, b, M1, M2, N1, N2, A_signs):
    c_new = common_to_canonical_calc_c(c, M1, N1, N2)
    A_new = common_to_canonical_calc_A(A, M1, M2, N1, N2)
    b_new = common_to_canonical_calc_b(b, M1, M2)
    return c_new, A_new, b_new, ['=' for i in range(len(A_signs))], [i for i in range(len(A_new[0]))]

def common_to_canonical_calc_c(c, M1, N1, N2):
    c_new = []
    for i in N1:
        c_new.append(c[i])
    for i in N2:
        c_new.append(c[i])
    for i in N2:
        c_new.append(-c[i])
    for i in M1:
        c_new.append(0)
    return np.array(c_new, float)


def common_to_canonical_calc_A(A, M1, M2, N1, N2):
    A_new = []
    for i in range(len(M1)):
        A_new.append([])
        for j in range(len(N1)):
            A_new[i].append(A[M1[i]][N1[j]])
        for j in range(len(N2)):
            A_new[i].append(A[M1[i]][N2[j]])
        for j in range(len(N2)):
            A_new[i].append(-A[M1[i]][N2[j]])
        for j in range(len(M1)):
            if i == j:
                A_new[i].append(-1)
            else:
                A_new[i].append(0)
    for i in range(len(M2)):
        A_new.append([])
        for j in range(len(N1)):
            A_new[i + len(M1)].append(A[M2[i]][N1[j]])
        for j in range(len(N2)):
            A_new[i + len(M1)].append(A[M2[i]][N2[j]])
        for j in range(len(N2)):
            A_new[i + len(M1)].append(-A[M2[i]][N2[j]])
        for j in range(len(M1)):
            A_new[i + len(M1)].append(0)
    return np.array(A_new, float)


def common_to_canonical_calc_b(b, M1, M2):
    b_new = []
    for i in M1:
        b_new.append(b[i])
    for i in M2:
        b_new.append(b[i])
    return np.array(b_new, float)

if __name__ == '__main__':
    A = [[2, 1, 3, 3, -1], [1, 2, 2, -2, -3], [3, 1, 1, 12, 3], [1, 1, 1, -2, -5], [1, 3, 1, 6, 8]]
    b = [24, 4, -3, 12, 8]
    c = [5, 6, 4, 1, 2, 0]  # the last is free coefficient

    A_signs_tmp = ['=', '=', '=', '<=', '>=']
    x_signs_tmp = [0, 1, 2]
    min_max_tmp = 'min'
    M1, M2, N1, N2, min_max_new = manager(c, A, b, A_signs_tmp, min_max_tmp, x_signs_tmp)

    c_new, A_new, b_new, new_asigns, new_xsigns = common_to_canonical(c, A, b, M1, M2, N1, N2, A_signs_tmp)
    brp = 0
