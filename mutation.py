from random import randint, sample, shuffle, random
from charles import Individual
from data.data_prep import nutrients, target_nutrients
import numpy as np


def flip_food(individual):
    """Selects a random segment of the chromosome and flips each gene: 0 to a random integer between 1 and 100, and non-zero values to 0.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    mut_indexes.sort()
    for gene in range(mut_indexes[0], mut_indexes[1]):
        if individual[gene] == 0:
            individual[gene] = randint(1, 100)
        else:
            individual[gene] = 0

    return individual


def swap_mutation(individual):
    """Selects a random segment of the chromosome and inverts segment order.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    individual[mut_indexes[0]], individual[mut_indexes[1]] = (
        individual[mut_indexes[1]],
        individual[mut_indexes[0]],
    )
    return individual


def inversion_mutation(individual):
    """Selects a random segment of the chromosome and inverts genes order.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    mut_indexes.sort()
    individual[mut_indexes[0] : mut_indexes[1]] = individual[
        mut_indexes[0] : mut_indexes[1]
    ][
        ::-1
    ]  # Inversion of string - makes it different from swap mut
    return individual


def shuffle_mutation(individual):
    """Selects a random segment of the chromosome and randomly shuffles the genes within that segment.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sorted(sample(range(0, len(individual)), 2))
    shuffled_chromosomes = individual[mut_indexes[0] : mut_indexes[1] + 1]
    shuffle(shuffled_chromosomes)
    individual[mut_indexes[0] : mut_indexes[1] + 1] = shuffled_chromosomes
    return individual


def shift_mutation(individual):
    """Shift mutation for a GA individual. Shifts a random portion of the representation
    by a random number of positions (between 1,5) to the left or to the right(50% chance).

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sorted(sample(range(0, len(individual)), 2))
    segment = individual[mut_indexes[0] : mut_indexes[1] + 1]
    shift = randint(1, 5)
    if randint(0, 1):
        # if 1 segments shifts to right
        segment = segment[shift:] + segment[:shift]
        # if 0 to the left
    else:
        segment = segment[-shift:] + segment[:-shift]
    individual[mut_indexes[0] : mut_indexes[1] + 1] = segment
    return individual


def add_or_remove_mutation(individual):
    """Selects between 1 to 20 genes and adjusts them by adding values (1 to 3) if nutrient content is
    below the target or sets genes to 0 if above the target.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    current_nutrients = np.dot(individual, nutrients)
    nutrient_diff = sum(current_nutrients - np.array(target_nutrients))
    mut_indexes = sample(range(0, len(individual)), randint(1, 20))

    counter = len(
        mut_indexes
    )  # makes it to iterate as many times as there are indexes to improve swap probability
    if nutrient_diff < 0:
        for i in mut_indexes:
            if counter > 0 and individual[i] == 0:
                individual[i] = randint(1, 3)
                counter -= 1

    elif nutrient_diff > 0:
        for i in mut_indexes:
            if counter > 0 and individual[i] > 0:
                individual[i] = 0
                counter -= 1
    return individual


def gaussian_adaptation_mutation(individual):
    """Randomly adds a value from a normal distribution (mean 0, standard deviation 10)
    to each gene with a 50% chance, ensuring values are within the range of 0 to 100.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mutated_individual = []
    for gene in individual:
        if random() < 0.5:
            mutated_value = int(np.round(gene + np.random.normal(0, 10)))
            mutated_value = max(
                0, min(100, mutated_value)
            )  # Ensure mutated value is within [0, 100]
            mutated_individual.append(mutated_value)
        else:
            mutated_individual.append(gene)
    return mutated_individual


def fitness_dependent_mutation(individual, mutation=swap_mutation, max_tries=5):
    """Applies a chosen mutation operator n times and selects the best individual based on fitness.

    Args:
        individual (Individual): A GA individual from charles.py
        mutation (function, optional): Mutation operator. Defaults to swap_mutation.
        max_tries (int, optional): Maximum number of tries. Defaults to 5.

    Returns:
        Individual: Mutated Individual
    """
    best_individual = [individual, Individual(individual).get_fitness()]
    # Mutate
    for i in range(1, max_tries + 1):
        mutated_representation = mutation(individual)
        mutated_individual = [
            mutated_representation,
            Individual(mutated_representation).get_fitness(),
        ]
        if mutated_individual[1] < best_individual[1]:  # Individuals fitness comparison
            best_individual = mutated_individual

    return best_individual[0]


if __name__ == "__main__":
    test = [0 for i in range(0, 76)] + [1]
    print(swap_mutation(test))
