from mutation import *
from selection import *
from xo import *
from charles import *
from fitness import *
import pandas as pd
import itertools
from tqdm import tqdm


def run_setup(
    pop_size,
    gens,
    selection_options,
    fitness_options,
    xo_options,
    xo_prob,
    mutation_options,
    mut_prob,
    file_name,
    **kwargs,
):

    results = pd.DataFrame(
        columns=[
            "fitness_func",
            "selection",
            "xo",
            "xo_prob",
            "mutation",
            "mut_prob",
            "run",
            "generation",
            "fitness",
            "final nutrients diff",
            "food variety",
        ]
    )
    results_list = []
    all_combinations = list(
        itertools.product(
            fitness_options, selection_options, xo_options, mutation_options
        )
    )
    total_iterations = len(all_combinations) * 30
    with tqdm(total=total_iterations, desc="Progress") as pbar:
        for run in range(1, 31):
            for combination in all_combinations:
                Individual.get_fitness = globals()[combination[0]]
                select_func = globals()[combination[1]]
                xo_func = globals()[combination[2]]
                mutate_func = globals()[combination[3]]
                pop = Population(
                    size=pop_size,
                    optim="min",
                    sol_size=len(nutrients),
                    valid_set=range(0, 101),
                    repetition=True,
                )
                evolve = pop.evolve(
                    gens=gens,
                    xo_prob=xo_prob,
                    mut_prob=mut_prob,
                    select=select_func,
                    xo=xo_func,
                    mutate=mutate_func,
                    elitism=True,
                    **kwargs,
                )

                for result in evolve:
                    results_list.append(
                        {
                            "fitness_func": combination[0],
                            "selection": combination[1],
                            "xo": combination[2],
                            "xo_prob": xo_prob,
                            "mutation": combination[3],
                            "mut_prob": mut_prob,
                            "run": run,
                            "generation": result[0],
                            "fitness": result[1],
                            "final nutrients diff": (
                                result[2] if len(result) > 2 else None
                            ),
                            "food variety": result[3] if len(result) > 3 else None,
                        }
                    )
                pbar.update(1)

        results = pd.DataFrame(results_list)
        results.to_csv(f"./results/{file_name}.csv", index=False)


def compare_tournament_size(
    pop,
    gens,
    selection_options,
    xo_options,
    xo_prob,
    mutation_options,
    mut_prob,
    tour_sizes,
    file_name,
):

    results = pd.DataFrame(
        columns=[
            "selection",
            "tour_size",
            "xo",
            "xo_prob",
            "mutation",
            "mut_prob",
            "run",
            "generation",
            "fitness",
        ]
    )
    results_list = []
    all_combinations = list(
        itertools.product(selection_options, xo_options, mutation_options, tour_sizes)
    )
    total_iterations = len(all_combinations) * 30
    with tqdm(total=total_iterations, desc="Progress") as pbar:
        for run in range(1, 31):
            for combination in all_combinations:
                select_func = globals()[combination[0]]
                xo_func = globals()[combination[1]]
                mutate_func = globals()[combination[2]]
                tour_size = combination[3]

                evolve = pop.evolve(
                    gens=gens,
                    xo_prob=xo_prob,
                    mut_prob=mut_prob,
                    select=select_func,
                    xo=xo_func,
                    mutate=mutate_func,
                    elitism=True,
                    tour_size=tour_size,
                )

                for result in evolve:
                    results_list.append(
                        {
                            "selection": combination[0],
                            "tour_size": combination[3],
                            "xo": combination[1],
                            "xo_prob": xo_prob,
                            "mutation": combination[2],
                            "mut_prob": mut_prob,
                            "run": run,
                            "generation": result[0],
                            "fitness": result[1],
                        }
                    )
                pbar.update(1)

        results = pd.DataFrame(results_list)
        results.to_csv(f"./results/{file_name}.csv", index=False)
