from data.data_prep import nutrients, prices, target_nutrients
from charles import *
from mutation import *
from selection import *
from xo import *
import numpy as np
import pandas as pd
import itertools
from tqdm import tqdm


def get_fitness(self):
    total_cost = np.dot(self.representation, prices)
    self.total_nutrients = np.dot(self.representation, nutrients)
    fitness = total_cost

    # if np.sum(self.representation) == 1:
    #     fitness += 1000

    # count_greater_than_one = np.sum(np.array(self.representation) > 0)
    # print(count_greater_than_one)

    nutrient_shortfall = np.maximum(target_nutrients - self.total_nutrients, 0)
    fitness += (
        np.sum(nutrient_shortfall) * 1000
    )  # multiply to ensure that sol doesn't contain nutrient deficits

    # nutrient_shortfall = np.sum(np.abs(target_nutrients - self.total_nutrients))
    # fitness += nutrient_shortfall * 1000

    return fitness


Individual.get_fitness = get_fitness


pop = Population(
    size=100,
    optim="min",
    sol_size=len(nutrients),
    valid_set=range(0, 101),
    repetition=True,
)


pop.evolve(
    gens=1000,
    xo_prob=0.85,
    mut_prob=0.15,
    select=fps,
    xo=cycle_xo,
    mutate=shuffle_mutation,
    elitism=True,
    tour_size=3,
    max_tries=10,
    k_point=10,
    uniform_prob=0.5,
)


#####   Results Comparison    #####
# select_list = ["fps", "tournament_sel", "rank_sel"]
# xo_list = ["single_point_xo"]
# mutate_list = ["swap_mutation"]


# def get_results(pop, gens, xo_prob, mut_prob, select_list, xo_list, mutate_list):
#     results = pd.DataFrame(
#         columns=["selection", "xo", "mutation", "run", "generation", "fitness"]
#     )
#     results_list = []

#     all_combinations = list(itertools.product(select_list, xo_list, mutate_list))
#     total_iterations = len(all_combinations) * 30
#     with tqdm(total=total_iterations, desc="Progress") as pbar:
#         for run in range(1, 31):
#             for combination in all_combinations:
#                 select_func = globals()[combination[0]]
#                 xo_func = globals()[combination[1]]
#                 mutate_func = globals()[combination[2]]

#                 evolve = pop.evolve(
#                     gens=gens,
#                     xo_prob=xo_prob,
#                     mut_prob=mut_prob,
#                     select=select_func,
#                     xo=xo_func,
#                     mutate=mutate_func,
#                     elitism=True,
#                 )

#                 for result in evolve:
#                     results_list.append(
#                         {
#                             "parameters": combination,
#                             "run": run,
#                             "generation": result[0],
#                             "fitness": result[1],
#                         }
#                     )
#                 pbar.update(1)

#         results = pd.DataFrame(results_list)
#         results.to_csv("./data/results.csv", index=False)


# get_results(pop, 500, 0.85, 0.15, select_list, xo_list, mutate_list)
