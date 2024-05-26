from random import randint, sample, shuffle, choice, random
from data.data_prep import nutrients, target_nutrients, prices
import numpy as np


def swap_mutation(individual):
    """Swap mutation for a GA individual. Swaps the bits.

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
    """Inversion mutation for a GA individual. Reverts a portion of the representation.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    mut_indexes.sort()
    individual[mut_indexes[0] : mut_indexes[1]] = individual[
        mut_indexes[0] : mut_indexes[1]
    ][::-1]
    return individual


def shuffle_mutation(individual):
    """Shuffle mutation for a GA individual. Shuffles a random portion of the representation.

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
    """Shift mutation for a GA individual. Shifts a random portion of the representation
    by a random number of positions (between 1,5) to the left or to the right(50% chance).

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """

    current_nutrients = np.dot(individual, nutrients)
    nutrient_diff = sum(current_nutrients - np.array(target_nutrients))
    mut_indexes = sample(range(0, len(individual)), randint(1, 10))

    counter = len(mut_indexes)
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
    mutated_individual = []
    for gene in individual:
        if random() < 0.15:  # 50% chance to mutate or keep the original gene
            mutated_value = int(np.round(gene + np.random.normal(0, 10)))
            mutated_value = max(
                0, min(100, mutated_value)
            )  # Ensure mutated value is within [0, 100]
            mutated_individual.append(mutated_value)
        else:
            mutated_individual.append(gene)  # Keep the original gene as integer
    return mutated_individual


def fitness(individual):
    total_cost = np.dot(individual, prices)
    total_nutrients = np.dot(individual, nutrients)
    fitness = total_cost
    nutrient_shortfall = np.maximum(target_nutrients - total_nutrients, 0)
    fitness += np.sum(nutrient_shortfall) * 1000
    return fitness


def fitness_dependent_swap(individual, max_tries=5):
    """Shift mutation for a GA individual. Shifts a random portion of the representation
    by a random number of positions (between 1,5) to the left or to the right(50% chance).

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    best_individual = [individual, fitness(individual)]
    # Mutate
    for i in range(1, max_tries + 1):
        mutated_representation = individual
        mutated_individual = [mutated_representation, fitness(mutated_representation)]
        if mutated_individual[1] < best_individual[1]:
            best_individual = mutated_individual

    return best_individual[0]


if __name__ == "__main__":
    test = [0 for i in range(0, 76)] + [1]
    print(gaussian_mutation(test))
