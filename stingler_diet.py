from data.data_prep import nutrients, prices, target_nutrients
from charles import *
from aux_funcs import *
from fitness import *
import numpy as np
from telegram_not import message
import glob


# # Comparing fitness functions

# fitness_options = [
#     "fitness_sum_excess_shortfall",
#     "fitness_sum_shortfall",
#     "fitness_each_shortfall",
#     "fitness_each_excess_shortfall",
#     "fitness_each_excess_shortfall_weighted",
# ]
# selection_options = ["fps"]
# xo_options = ["single_point_xo"]
# mutation_options = ["swap_mutation"]

# print("Running Fitness functions comparison")
# run_setup(
#     pop_size=100,
#     gens=1000,
#     fitness_options=fitness_options,
#     selection_options=selection_options,
#     xo_options=xo_options,
#     xo_prob=0.8,
#     mutation_options=mutation_options,
#     mut_prob=0.15,
#     file_name="fitness_funcs__comparison",
# )
# message()

# # Comparing xo operators

# fitness_options = [
#     "fitness_each_shortfall",
# ]
# selection_options = ["fps"]
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
# mutation_options = ["swap_mutation"]

# print("Running Xo operators comparison")
# run_setup(
#     pop_size=100,
#     gens=1000,
#     fitness_options=fitness_options,
#     selection_options=selection_options,
#     xo_options=xo_options,
#     xo_prob=0.8,
#     mutation_options=mutation_options,
#     mut_prob=0.15,
#     file_name="xo__comparison",
# )
# message()

## Comparing xo operators inside fitness dependent xo

# fitness_options = [
#     "fitness_each_shortfall",
# ]
# selection_options = ["fps"]
# xo_options = ["fitness_dependent_xo"]
# mutation_options = ["swap_mutation"]
# fitness_dependent_xo_options = [
#     single_point_xo,
#     k_point_xo,
#     uniform_xo,
#     adapted_pmx,
#     ordered_xo,
#     cycle_xo,
#     int_arithmetic_crossover,
# ]


# for i,option in enumerate(fitness_dependent_xo_options):
#     print(f"Running Fitness dependent XO operators comparison: {i}/{len(fitness_dependent_xo_options)}")
#     run_setup(
#         pop_size=100,
#         gens=100,
#         fitness_options=fitness_options,
#         selection_options=selection_options,
#         xo_options=xo_options,
#         xo_prob=0.8,
#         mutation_options=mutation_options,
#         mut_prob=0.15,
#         file_name=f"fitness_dependent_{option.__name__}",
#         fitness_dependent_xo_var=option,
#     )

# concatenate_csv_files(
#     prefix="fitness_dependent_", output_file_name="fitness_dependent_comparison"
# )
# message()


# Comparing POP sizes

# fitness_options = ["fitness_each_shortfall"]
# selection_options = ["fps"]
# xo_options = ["fitness_dependent_xo"]
# mutation_options = ["swap_mutation"]

# pop_sizes = [i if i != 0 else 10 for i in range(0, 511, 50)]

# for i,pop_size in enumerate(pop_sizes):
#     print(f"Run for pop size:{pop_size} ({i}/{len(pop_sizes)}) ")
#     run_setup(
#         pop_size=pop_size,
#         gens=100,
#         fitness_options=fitness_options,
#         selection_options=selection_options,
#         xo_options=xo_options,
#         xo_prob=0.8,
#         mutation_options=mutation_options,
#         mut_prob=0.15,
#         fitness_dependent_xo_var=uniform_xo,
#         file_name=f"pop_{pop_size}",
#     )

# concatenate_csv_files_col_names(prefix="pop_", output_file_name="pop_size_comparison")
# message()


# # Comparing XO prob

# fitness_options = ["fitness_each_shortfall"]
# selection_options = ["fps"]
# xo_options = ["fitness_dependent_xo"]
# mutation_options = ["swap_mutation"]

# xo_probs = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
# for i,proba in enumerate(xo_probs):
#     print(f"Run for proba:{proba} ({i}/{len(xo_probs)}) ")
#     run_setup(
#         pop_size=100,
#         gens=100,
#         fitness_options=fitness_options,
#         selection_options=selection_options,
#         xo_options=xo_options,
#         xo_prob=proba,
#         mutation_options=mutation_options,
#         mut_prob=0.15,
#         fitness_dependent_xo_var=uniform_xo,
#         file_name=f"xo-prob_{proba}",
#     )

# concatenate_csv_files_col_names(
#     prefix="xo-prob_", output_file_name="xo_proba_comparison"
# )
# message()


# ## Comparing tours size

# fitness_options = ["fitness_each_shortfall"]
# selection_options = ["tournament_sel"]
# xo_options = ["fitness_dependent_xo"]
# mutation_options = ["swap_mutation"]

# tour_sizes = [i for i in range(2, 21, 2)]

# for i,size in enumerate(tour_sizes):
#     print(f"Run for size:{size} ({i}/{len(tour_sizes)}) ")
#     run_setup(
#         pop_size=100,
#         gens=100,
#         fitness_options=fitness_options,
#         selection_options=selection_options,
#         xo_options=xo_options,
#         xo_prob=0.85,
#         mutation_options=mutation_options,
#         mut_prob=0.15,
#         fitness_dependent_xo_var=uniform_xo,
#         tour_size=size,
#         file_name=f"tournament_size_{i}",
#     )

# concatenate_csv_files(
#     prefix="tournament_size", output_file_name="tournament_size_comparison"
# )
# message()


# Comparing Selection operators

# fitness_options = ["fitness_each_shortfall"]
# selection_options = ["fps", "tournament_sel", "rank_sel"]
# xo_options = ["fitness_dependent_xo"]
# mutation_options = ["swap_mutation"]

# print("Running Selection operator comparison")
# run_setup(
#     pop_size=100,
#     gens=1000,
#     fitness_options=fitness_options,
#     selection_options=selection_options,
#     xo_options=xo_options,
#     xo_prob=0.85,
#     mutation_options=mutation_options,
#     mut_prob=0.15,
#     fitness_dependent_xo_var=uniform_xo,
#     tour_size=4,
#     file_name=f"selection_comparison",
# )
# message()

#  Comparing Mutation Operators

fitness_options = ["fitness_each_shortfall"]
selection_options = ["tournament_sel"]
xo_options = ["fitness_dependent_xo"]
mutation_options = [
    "flip_food",
    "swap_mutation",
    "inversion_mutation",
    "shuffle_mutation",
    "shift_mutation",
    "add_or_remove_mutation",
    "gaussian_adaptation_mutation",
    "fitness_dependent_mutation",
]

print("Running Mutation operator comparison")
run_setup(
    pop_size=100,
    gens=1000,
    fitness_options=fitness_options,
    selection_options=selection_options,
    xo_options=xo_options,
    xo_prob=0.85,
    mutation_options=mutation_options,
    mut_prob=0.15,
    fitness_dependent_xo_var=uniform_xo,
    tour_size=4,
    file_name=f"mutation_comparison",
)

message()
