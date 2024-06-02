from mutation import *
from selection import *
from xo import *
from charles import *
from fitness import *
import pandas as pd
import itertools
from tqdm import tqdm
import glob
import os


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
    """
    Enables to define lists of genetic operators, create all possible combinations and plug
    them to the evolve function of the population class. Saves a csv file with the results.
    """
    # Results storing df
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
            "Additional info",
        ]
    )
    results_list = []
    # List of all possible combinations
    all_combinations = list(
        itertools.product(
            fitness_options, selection_options, xo_options, mutation_options
        )
    )
    total_iterations = len(all_combinations) * 30
    with tqdm(total=total_iterations, desc="Progress") as pbar:
        for run in range(1, 31):  # runs each combination 30 times
            for combination in all_combinations:
                Individual.get_fitness = globals()[
                    combination[0]
                ]  # Monkey patches the fitness function
                # Converts functions name string to function object
                select_func = globals()[combination[1]]
                xo_func = globals()[combination[2]]
                mutate_func = globals()[combination[3]]
                # Defines population class (pop size gets passed as an argument)
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
                    **kwargs,  # accepts additional parameters for the xo and mutation functions (eg. fitness_dependent_xo_var)
                )
                kwargs_dict = {
                    key: (value.__name__ if callable(value) else value)
                    for key, value in kwargs.items()
                }
                # Records all run data in a dict and appends it to the results df
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
                            "Additional info": kwargs_dict,
                        }
                    )
                pbar.update(1)

        results = pd.DataFrame(results_list)
        results.to_csv(f"./results/{file_name}.csv", index=False)


def concatenate_csv_files(prefix, output_file_name):
    """
    Workaround to not make the setup function more complex
    Some additional arguments like tournament size and xo probability aren't passed as list like the operators.
    Instead, for each value the run_setup function is called, resulting in multiple csv files with a common prefix.
    This function combines all the files with the same prefix into one.
    """
    files = glob.glob(f"./results/{prefix}*.csv")
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv(f"./results/{output_file_name}.csv", index=False)
    for file in files:
        os.remove(file)


def concatenate_csv_files_col_names(prefix, output_file_name):
    """
    Same logic as the previous function but for cases where the run_setup function doesn't store the variable being tested.
    For example, population size isn't tracked, but that info is stored in the file name along with a prefix.
    This function create a column with the variable being tested value and combines all the files with the same prefix into one.
    Resulting in a single file with an extra col that features the variable being tested.
    """
    files = glob.glob(f"./results/{prefix}*.csv")
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        base_name = os.path.splitext(os.path.basename(file))[0]
        col_name = base_name.split("_")[0]
        df[col_name] = base_name.split("_")[1]
        dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv(f"./results/{output_file_name}.csv", index=False)
    for file in files:
        os.remove(file)
