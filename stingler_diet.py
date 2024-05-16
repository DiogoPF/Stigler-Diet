from data.data_prep import nutrients, prices, target_nutrients
from class_code.charles import *
from class_code.mutation import *
from class_code.selection import *
from class_code.xo import *
import numpy as np
import numpy as np


def get_fitness(self):
    total_cost = np.dot(self.representation, prices)
    self.total_nutrients = np.dot(self.representation, nutrients)
    fitness = total_cost

    nutrient_shortfall = np.maximum(target_nutrients - self.total_nutrients, 0)
    fitness += np.sum(nutrient_shortfall)

    return fitness


# def get_fitness(self):
#     total_cost = np.dot(self.representation, prices)
#     total_nutrients = np.dot(self.representation, nutrients)
#     fitness = total_cost

#     for nutrient in target_nutrients:
#         for i in total_nutrients:
#             if i < nutrient:
#                 fitness += abs(nutrient - i)

#     return fitness


Individual.get_fitness = get_fitness

pop = Population(
    size=100,
    optim="min",
    sol_size=len(nutrients),
    valid_set=[0, 1],
    repetition=True,
)


pop.evolve(
    gens=100,
    xo_prob=0.85,
    mut_prob=0.15,
    select=fps,
    xo=single_point_xo,
    mutate=binary_mutation,
    elitism=True,
)
