from pulp import *
import time

values = range(1,10)
rows = range(1,10)
cols = range(1,10)

boxes = [[(3*i+k+1, 3*j+l+1) for k in range(3) for l in range(3)] for i in range(3) for j in range(3)]

prob = LpProblem("sudoku")

# 1 if value v is in position (r,c), zero otherwise
decision_vars = LpVariable.dicts("var", (values, rows, cols), cat='Binary')

###### Constraints

# One value per space
for r in rows:
    for c in cols:
        prob += lpSum([decision_vars[v][r][c]] for v in values) == 1

# One of each value in each row/col/box
for v in values:
    for r in rows:
        prob += lpSum([decision_vars[v][r][c] for c in cols]) == 1
    for c in cols:
        prob += lpSum([decision_vars[v][r][c] for r in rows]) == 1
    for b in boxes:
        prob += lpSum([decision_vars[v][r][c] for (r,c) in b]) == 1

# problem data (as val, row, col pairs)
# problem source: https://www.youtube.com/watch?v=9m9t8ie9-EE

prob_data = [
    (5,1,1),
    (2,1,4),
    (4,1,8),
    (6,2,4),
    (3,2,6),
    (3,3,2),
    (9,3,6),
    (7,3,9),
    (3,4,3),
    (7,4,6),
    (7,5,3),
    (8,5,6),
    (6,6,1),
    (2,6,8),
    (8,7,2),
    (3,7,9),
    (4,8,4),
    (6,8,7),
    (1,9,4),
    (5,9,7)
]

# add problem data as constraints

for (v,r,c) in prob_data:
    prob += decision_vars[v][r][c] == 1

start_time = time.time()

prob.solve()

end_time = time.time()

# print solution

print(f'Solved for {81 - len(prob_data)} unknowns in {(end_time - start_time):.2f} seconds. Initial problem was:\n')

for r in rows:
    if r in [1,4,7]:
        print("-------------------------\n", end='')
    for c in cols:
        inprob = False
        if c in [1,4,7]:
            print("| ", end='')
        for v in values:
            if (v,r,c) in prob_data:
                print("\033[1m" + str(v) + " " + "\033[0m", end='')
                inprob = True;
                break
        if inprob == False:
            print("  ", end='')
        if c == 9:
            print("|\n", end='')
print("-------------------------\n", end='')

print("\nSolution is:\n")

for r in rows:
    if r in [1,4,7]:
        print("-------------------------\n", end='')
    for c in cols:
        for v in values:
            if value(decision_vars[v][r][c]) == 1:
                if c in [1,4,7]:
                    print("| ", end='')
                if (v,r,c) in prob_data:
                    print("\033[1m" + str(v) + " " + "\033[0m", end='')
                else:    
                    print(f'{v} ', end='')
                if c == 9:
                    print("|\n", end='')
print("-------------------------\n", end='')


