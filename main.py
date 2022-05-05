import numpy as np
import heapq
import queue
import wezel
import sys

"""
holder = sys.argv[0]
algorytm = str(sys.argv[1])
operandy = str(sys.argv[2])
plik = str(sys.argv[3])
plik_sol = str(sys.argv[4])
plik_stats = str(sys.argv[5])
"""
plik = "4x4_06_00003.txt"
plik_sol = "sol.txt"
operandy = "RLUD"

file = open(plik, "r")

M = int(file.read(1))
file.read(1)
N = int(file.read(1))

file.read(1)

m = np.loadtxt(plik, dtype='d', delimiter=' ', skiprows=1)


def generateG():
    licznik = 1
    tmp = []
    wynik = []
    for i in range(M):
        for j in range(N):
            tmp.append(licznik)
            licznik += 1
        wynik.append(tmp.copy())
        tmp.clear()
    wynik[M-1][N-1] = 0
    return wezel.Wezel(wynik, "", M, N)


G = generateG()
s = wezel.Wezel(m, "", M, N)


def bfs(G, s):
    if G.isGoal(s):
        with open(plik_sol, 'w') as file:
            file.write(str(len(s.get_operators()))+'\n')
            file.write(s.get_operators())
            print(s.get_operators())
        return "Success"
    Q = queue.Queue()
    U = set()
    Q.put(s)
    U.add(s)
    while not Q.empty():
        v = Q.get()
        for n in v.neighbours(operandy):
            if n == '-':
                continue
            if G.isGoal(n):
                with open(plik_sol, 'w') as file:
                    file.write(str(len(n.get_operators()))+'\n')
                    file.write(n.get_operators())
                    print(n.get_operators())
                return "Success"
            flaga = False
            for u in U:
                if u.isGoal(n):
                    flaga = True
                    break
            if not flaga:
                Q.put(n)
                U.add(n)
    with open(plik_sol, 'w') as file:
        file.write("-1")
    return "Failure"


def dfs(G, s):
    o = operandy[::-1]
    if G.isGoal(s):
        with open("dfs_sol.txt", 'w') as file:
            file.write(str(len(s.get_operators()))+'\n')
            file.write(s.get_operators())
            print(s.get_operators())
        return "Success"
    S = []
    T = set()
    S.append(s)
    while len(S) != 0:
        v = S.pop()
        flaga = False
        for t in T:
            if t.isGoal(v):
                flaga = True
                break
        if not flaga:
            T.add(v)
            for n in v.neighbours(o):
                if n == '-':
                    continue
                if n.get_deep() <= v.get_deep():
                    n.set_deep(v.get_deep())
                if n.get_deep() >= 20:
                    continue
                if G.isGoal(n):
                    with open("dfs_sol.txt", 'w') as file:
                        file.write(str(len(n.get_operators())) + '\n')
                        file.write(n.get_operators())
                        print(n.get_operators())
                    return "Success"
                S.append(n)
    with open("dfs_sol.txt", 'w') as file:
        file.write("-1")
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
    m = [[1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]]
    for i in range(M):
        for j in range(N):
            if m[i][j] != v.matrix[i][j]:
                wynik += 1
    return wynik


def Manhattan(v):
    tab = wezel.find_zero(v.get_matrix(), M, N)
    return (M - 1 - tab[0]) + (N - 1 - tab[0])


def Astar(G, s, heurystyka):
    if G.isGoal(s):
        with open(plik_sol, 'w') as file:
            file.write(str(len(s.get_operators())) + '\n')
            file.write(s.get_operators())
        print(s.get_operators())
        return "Success"
    P = queue.PriorityQueue()
    T = set()
    P.put((0, s))
    s.set_priority(0)
    while not P.empty():
        v = P.get()[1]
        if G.isGoal(v):
            with open(plik_sol, 'w') as file:
                file.write(str(len(v.get_operators())) + '\n')
                file.write(v.get_operators())
            print(v.get_operators())
            return "Success"
        T.add(v)
        for n in v.neighbours("LDUR"):
            if n == '-':
                continue
            n.set_deep(v.get_deep())
            flaga = False
            for t in T:
                if t.isGoal(n):
                    flaga = True
                    break
            if not flaga:
                if not is_in_queue(n, P):
                    f = n.get_deep() + heurystyka(v)
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
    return "Failure"


print(bfs(G, s))

print(dfs(G, s))

print(Astar(G, s, Huminga))

print(Astar(G, s, Manhattan))
