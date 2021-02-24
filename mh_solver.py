import random
import time
import math
import numpy as np
import copy

# Metaheuristic sudoku solver

# Problem representation

prob = np.array([
    [5,0,0,2,0,0,0,4,0],
    [0,0,0,6,0,3,0,0,0],
    [0,3,0,0,0,9,0,0,7],
    [0,0,3,0,0,7,0,0,0],
    [0,0,7,0,0,8,0,0,0],
    [6,0,0,0,0,0,0,2,0],
    [0,8,0,0,0,0,0,0,3],
    [0,0,0,4,0,0,6,0,0],
    [0,0,0,1,0,0,5,0,0],
])

# Tuning parameters
weights = [1,1,1,1] # Weights for objective function [prob_data error, rows_error, cols_error, boxes_error]
parent_prop = 0.5
pop_size = 100

assert((parent_prop*pop_size).is_integer()) # Check that a whole number of parents are selected
assert((parent_prop*pop_size/2).is_integer()) # Check that selected parents can be paired evenly

# prob data error (diff between problem and current sol for given values)
def prob_data_error(prob, sol):
    prob_data_error = 0
    for i in range(9):
        for j in range(9):
            if prob[i][j] != 0:
                prob_data_error += (sol[i][j] - prob[i][j])**2
    return prob_data_error

def rows_error(sol):
    error_sum = 0
    for i in range(9):
        for j in range(1,10):
            error_sum += abs(1 - (sol[i]==j).sum())
    return error_sum**2

def cols_error(sol):
    error_sum = 0
    for i in range(9):
        for j in range(1,10):
            error_sum += abs(1 - (sol[:][i]==j).sum())
    return error_sum**2

def boxes_error(sol):
    error_sum = 0
    for i in range(3):
        for j in range(3):
            for k in range(1,10):
                count = 0
                for a in range(3*i,3*i+3):
                    for b in range(3*j, 3*j+3):
                        if sol[a][b] == k:
                            count += 1
                error_sum += abs(1 - count)
    return error_sum^2




# Objective function (minimization)
def objective(sol, weights):
    return weights[0]*prob_data_error(prob, sol) + weights[1]*rows_error(sol) + weights[2]*cols_error(sol) + weights[3]*boxes_error(sol)

# Create starting population
sols = np.zeros((pop_size,9,9))
for i in range(pop_size):
    sols[i][:][:] = copy.deepcopy(prob)
    for j in range(9):
        for k in range(9):
            if sols[i][j][k] == 0:
                sols[i][j][k] = random.randint(1,9)

print("Population created")

# Rank sols by fitness using objective
fitness = np.zeros((pop_size,2))
for i in range(len(sols)):
    fitness[i,0] = objective(sols[i], weights)
sum_fitness = np.sum(fitness,axis=0)[0]
for j in range(len(sols)):
    fitness[j,1] = fitness[j,0]/sum_fitness

# Choose parent population
temp_sols = np.zeros((int(len(sols)*parent_prop),9,9))
temp_fitness = np.zeros((int(len(sols)*parent_prop),2))
index = np.argsort(fitness[:,1], axis=0)
i = 0
count = 0
while count < len(sols)*parent_prop:
    if random.random() < fitness[index[i],1]:
        temp_sols[count][:][:] = copy.deepcopy(sols[index[i]])
        temp_fitness[count][:] = copy.deepcopy(fitness[index[i]])
        count += 1
    i += 1
    if i == pop_size:
        i = 0
    
print("Finished parent selection\n")

# Pair selected parents and perform crossover to create offspring

# Perform mutation on offspring