from data.data_prep import nutrients, prices, target_nutrients
from charles import *
from aux_funcs import *
from fitness import *
import numpy as np


# Individual.get_fitness = fitness_each_shortfall


# pop = Population(
#     size=100,
#     optim="min",
#     sol_size=len(nutrients),
#     valid_set=range(0, 101),
#     repetition=True,
# )


# pop.evolve(
#     gens=10,
#     xo_prob=0.85,
#     mut_prob=0.15,
#     select=fps,
#     xo=single_point_xo,
#     mutate=swap_mutation,
#     elitism=True,
# )
# fitness_options = [
#     "fitness_sum_excess_shortfall",
#     "fitness_sum_shortfall",
#     "fitness_each_shortfall",
#     "fitness_each_excess_shortfall",
#     "fitness_each_excess_shortfall_weighted",
# ]
# selection_options = ["fps", "rank_sel", "tournament_sel"]

# xo_options = [
#     "single_point_xo",
#     "k_point_xo",
#     "uniform_xo",
#     "adapted_pmx",
#     "ordered_xo",
#     "average_xo",
#     "cycle_xo",
#     "int_arithmetic_crossover",
#     "fitness_dependent_xo",
# ]

# mutation_options = [
#     "flip_food",
#     "swap_mutation",
#     "inversion_mutation",
#     "shuffle_mutation",
#     "shift_mutation",
#     "add_or_remove_mutation",
#     "gaussian_adaptation_mutation",
#     "fitness_dependent_mutation",
# ]
#########################################____Results Comparison____#########################################

# Comparing selection methods
fitness_options = [
    "fitness_sum_excess_shortfall",
]
selection_options = ["tournament_sel"]
xo_options = ["single_point_xo"]
mutation_options = ["swap_mutation"]


run_setup(
    pop_size=100,
    gens=100,
    fitness_options=fitness_options,
    selection_options=selection_options,
    xo_options=xo_options,
    xo_prob=0.8,
    mutation_options=mutation_options,
    mut_prob=0.15,
    file_name="all_results",
)

# Comparing Tournament Sizes

selection_options = ["tournament_sel"]
xo_options = ["single_point_xo"]
mutate_options = ["swap_mutation"]
tour_sizes = range(2, 11)

# compare_tournament_size(
#     pop=pop,
#     gens=500,
#     selection_options=selection_options,
#     xo_options=xo_options,
#     xo_prob=0.8,
#     mutation_options=mutate_options,
#     mut_prob=0.15,
#     tour_sizes=tour_sizes,
#     file_name="tournament_size_comparison",
# )


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
