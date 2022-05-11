import datetime
import numpy as np
import queue
import wezel
import sys
"""
plik = "4x4_03_00001.txt"
operandy = "LURD"
algorytm = "dfs"
plik_sol = "plik_sol.txt"
plik_stats = "plik_stats.txt"
"""
holder = sys.argv[0]
algorytm = str(sys.argv[1])
operandy = str(sys.argv[2])
plik = str(sys.argv[3])
plik_sol = str(sys.argv[4])
plik_stats = str(sys.argv[5])


file = open(plik, "r")

M = int(file.read(1))
file.read(1)
N = int(file.read(1))

file.read(1)

m = np.loadtxt(plik, dtype='d', delimiter=' ', skiprows=1)


def find_zero(m, M, N):
    for i in range(M):
        for j in range(N):
            if m[i][j] == 0:
                return [i, j]
    return [0, 0]


def generateG():
    licznik = 1
    wynik = np.zeros((4, 4))
    for i in range(M):
        for j in range(N):
            wynik[i][j] = licznik
            licznik += 1.
    wynik[M-1][N-1] = 0.
    return wezel.Wezel(wynik, find_zero(wynik, M, N), "", M, N)


G = generateG()
s = wezel.Wezel(m, find_zero(m, M, N), "", M, N)


def bfs(G, s):
    countOdw = 1
    countPrz = 0
    maxDepth = 0

    if G.isGoal(s):
        with open(plik_sol, 'w') as file:
            file.write(str(len(s.get_operators()))+'\n')
            file.write(s.get_operators())
        with open(plik_stats, 'w') as file:
            file.write(str(len(s.get_operators()))+'\n')
            file.write("1\n")
            file.write("0\n")
            file.write("0\n")
        return "Success"
    Q = queue.Queue()
    U = dict()
    Q.put(s)
    U[s.get_hash()] = s
    while not Q.empty():
        v = Q.get()
        countPrz += 1
        for n in v.neighbours(operandy):
            if n == '-':
                continue
            n.set_deep(v.get_deep())
            maxDepth = max(maxDepth, n.get_deep())
            if G.isGoal(n):
                with open(plik_sol, 'w') as file:
                    file.write(str(len(n.get_operators()))+'\n')
                    file.write(n.get_operators())
                with open(plik_stats, 'w') as file:
                    file.write(str(len(n.get_operators())) + '\n')
                    file.write(str(countOdw) + '\n')
                    file.write(str(countPrz) + '\n')
                    file.write(str(maxDepth) + '\n')
                return "Success"
            if not (n.get_hash() in U):
                Q.put(n)
                U[n.get_hash()] = n

    with open(plik_sol, 'w') as file:
        file.write("-1")
    with open(plik_stats, 'w') as file:
        file.write("-1" + '\n')
        file.write(str(countOdw)+'\n')
        file.write(str(countPrz)+'\n')
        file.write(str(maxDepth) + '\n')
    return "Failure"


def dfs(G, s):
    countOdw = 1
    countPrz = 0
    maxDepth = 0
    o = operandy[::-1]
    if G.isGoal(s):
        with open(plik_sol, 'w') as file:
            file.write(str(len(s.get_operators()))+'\n')
            file.write(s.get_operators())
        with open(plik_stats, 'w') as file:
            file.write(str(len(s.get_operators()))+'\n')
            file.write('1\n')
            file.write('0\n')
            file.write('0\n')
        return "Success"
    S = []
    T = dict()
    S.append(s)
    while len(S) != 0:
        v = S.pop()
        countPrz += 1
        if not (v.get_hash() in T):
            T[v.get_hash()] = v
            for n in v.neighbours(o):
                if n == '-':
                    continue
                if n.get_deep() <= v.get_deep():
                    n.set_deep(v.get_deep())
                if n.get_deep() > 20:
                    continue
                maxDepth = max(maxDepth, n.get_deep())
                if G.isGoal(n):
                    with open(plik_sol, 'w') as file:
                        file.write(str(len(n.get_operators())) + '\n')
                        file.write(n.get_operators())
                    with open(plik_stats, 'w') as file:
                        file.write(str(len(n.get_operators())) + '\n')
                        file.write(str(countOdw)+'\n')
                        file.write(str(countPrz)+'\n')
                        file.write(str(maxDepth)+'\n')
                    return "Success"
                S.append(n)
                countOdw += 1
    with open(plik_sol, 'w') as file:
        file.write("-1")
    with open(plik_stats, 'w') as file:
        file.write("-1\n")
        file.write(str(countOdw) + '\n')
        file.write(str(countPrz) + '\n')
        file.write(str(maxDepth) + '\n')
    return "Failure"


def is_in_queue(x, q):
   with q.mutex:
      return x in q.queue


def findIndex(q, n):
    for i in range(q):
        if q[i][1].isGoal(n):
            return
    return 0


def Huminga(v):
    wynik = 0
    m = G.get_matrix()
    for i in range(M):
        for j in range(N):
            if m[i][j] != v.matrix[i][j]:
                wynik += 1
    return wynik


def Manhattan(v):
    tab = v.get_zero()
    return (M - 1 - tab[0]) + (N - 1 - tab[1])


def Astar(G, s, heurystyka):
    countOdw = 1
    countPrz = 0
    maxDepth = 0
    if G.isGoal(s):
        with open(plik_sol, 'w') as file:
            file.write(str(len(s.get_operators())) + '\n')
            file.write(s.get_operators())
        with open(plik_stats, 'w') as file:
            file.write(str(len(s.get_operators()))+'\n')
            file.write("1\n")
            file.write("0\n")
            file.write("0\n")
        return "Success"
    P = queue.PriorityQueue()
    T = dict()
    P.put((0, s))
    s.set_priority(0)
    while not P.empty():
        v = P.get()[1]
        maxDepth = max(maxDepth, v.get_deep())
        if G.isGoal(v):
            with open(plik_sol, 'w') as file:
                file.write(str(len(v.get_operators())) + '\n')
                file.write(v.get_operators())
            with open(plik_stats, 'w') as file:
                file.write(str(len(v.get_operators())) + '\n')
                file.write(str(countOdw) + '\n')
                file.write(str(countPrz) + '\n')
                file.write(str(maxDepth) + '\n')
            return "Success"
        T[v.get_hash] = v
        countPrz += 1
        for n in v.neighbours("LDUR"):
            if n == '-':
                continue
            n.set_deep(v.get_deep())

            if not (n.get_hash in T):
                f = n.get_deep() + heurystyka(v)
                if not is_in_queue(n, P):
                    countOdw += 1
                    P.put((f, n))
                    n.set_priority(f)
                else:
                    if n.get_priority() > f:
                        tmp = []
                        while tmp[-1][1].isGoal(n):
                            tmp.append(P.get)
                        for i in range(0, len(tmp)-2):
                            P.put(tmp[i])
                        P.put((f, n))
                        n.set_priority(f)
    with open(plik_sol, 'w') as file:
        file.write("-1")
    with open(plik_stats, 'w') as file:
        file.write("-1")
        file.write(str(countOdw) + '\n')
        file.write(str(countPrz) + '\n')
        file.write(str(maxDepth) + '\n')
    return "Failure"



def main():
    start = datetime.datetime.now()
    if algorytm == "bfs":
        bfs(G, s)
    if algorytm == "dfs":
        dfs(G, s)
    if algorytm == "astr":
        if operandy == "hamm":
            Astar(G, s, Huminga)
        if operandy == "manh":
            Astar(G, s, Manhattan)
    end = datetime.datetime.now()
    czas = round((end - start).total_seconds() * 1000, 3)
    with open(plik_stats, 'a') as file:
        file.write(str(czas) + '\n')


main()
