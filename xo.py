from random import randint, sample, uniform, random, shuffle
from charles import Individual


def single_point_xo(parent1, parent2):
    """Implementation of single point crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_point = randint(1, len(parent1) - 1)
    offspring1 = parent1[:xo_point] + parent2[xo_point:]
    offspring2 = parent2[:xo_point] + parent1[xo_point:]
    return offspring1, offspring2


def k_point_xo(parent1, parent2, k=4):
    """Implementation of k-point crossover. Selects k random xo points and swaps the genes between the parents

    Args:
        parent1 (list of int): First parent for crossover.
        parent2 (list of int): Second parent for crossover.
        k (int, optional): Number of crossover points. Defaults to 4.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    xo_points = sample(range(1, len(parent1) - 1), k)
    xo_points.append(0)
    xo_points.append(len(parent1))
    xo_points = sorted(xo_points)
    offspring1 = list(parent1)
    offspring2 = list(parent2)
    for i in range(0, k + 1):
        if i % 2 == 0:
            continue
        offspring1[xo_points[i] : xo_points[i + 1]] = parent2[
            xo_points[i] : xo_points[i + 1]
        ]
        offspring2[xo_points[i] : xo_points[i + 1]] = parent1[
            xo_points[i] : xo_points[i + 1]
        ]
    return offspring1, offspring2


def uniform_xo(parent1, parent2, prob=0.5):
    """Implementation of uniform crossover.
    Swaps genes between the two parents with a given probability to create offspring.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.
        prob (float, optional): Crossover probability. Defaults to 0.5.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    offspring1 = list(parent1)
    offspring2 = list(parent2)
    for i in range(len(parent1)):
        if uniform(0, 1) < prob:
            offspring1[i] = parent2[i]
            offspring2[i] = parent1[i]
    return offspring1, offspring2


def adapted_pmx(parent1, parent2):
    """Implementation of adapted partially matched/mapped crossover.
    Exchanges segments between parents based on two random crossover points but does not ensure the uniqueness of genes in the offspring

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_points = sample(range(len(parent1)), 2)
    xo_points.sort()

    # Maintains parent genes, only window is swapped
    # Tried reversing the two segments before and after window but reveled to chromosome destructive
    offspring1 = (
        parent1[: xo_points[0]]  # [::-1]
        + parent2[xo_points[0] : xo_points[1]]
        + parent1[xo_points[1] :]  # [::-1]
    )

    offspring2 = (
        parent2[: xo_points[0]]  # [::-1]
        + parent1[xo_points[0] : xo_points[1]]
        + parent2[xo_points[1] :]  # [::-1]
    )

    return offspring1, offspring2


def ordered_xo(parent1, parent2):
    """Similar to the classical approach  of ordered crossover, but utilizes index-based operations to perform crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    index = [i for i in range(0, len(parent1))]
    xo_points = sample(range(len(parent1)), 2)
    xo_points.sort()
    start_index, end_index = xo_points[0], xo_points[1]

    offspring1, offspring2 = [None] * len(parent1), [None] * len(parent1)
    offspring1[start_index:end_index] = parent2[index[start_index] : index[end_index]]
    offspring2[start_index:end_index] = parent1[index[start_index] : index[end_index]]

    parent1_no_window = parent1[:start_index] + parent1[end_index:]
    parent2_no_window = parent2[:start_index] + parent2[end_index:]
    counter1 = end_index

    for value in parent1_no_window:
        offspring1[counter1 % len(parent1)] = value
        counter1 += 1

    counter2 = end_index
    for value in parent2_no_window:
        offspring2[counter2 % len(parent2)] = value
        counter2 += 1

    return offspring1, offspring2


def average_xo(parent1, parent2):
    """Calculates the average of each parents genes and rounds it to the nearest integer.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individual: One offspring, resulting from the crossover.
    """
    offspring = [int(parent1[i] + parent2[i] / 2) for i in range(len(parent1))]
    return offspring


def cycle_xo(p1, p2):
    """Similar to the classical approach (implemented in class) of cycle crossover, but utilizes index-based operations to perform crossover.
    The indexes are attributed randomly to each parent.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    p1_indexes = list(range(len(p1)))
    p2_indexes = list(range(len(p1)))
    shuffle(p1_indexes)
    shuffle(p2_indexes)

    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)

    while None in offspring1:
        index = offspring1.index(None)
        val1 = p1_indexes[index]
        val2 = p2_indexes[index]

        # copy the cycle elements
        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2_indexes[index]
            index = p1_indexes.index(val2)

        # copy the rest
        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return offspring1, offspring2


def int_arithmetic_crossover(p1, p2):
    """Similar to classical arithmetic crossover but uses a rounded-to-the-nearest-integer approach.

    Args:
        p1 (list of int): First parent for crossover.
        p2 (list of int): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    offspring1 = []
    offspring2 = []

    for i in range(len(p1)):
        r1 = random()
        r2 = random()
        offspring_value1 = round(p1[i] * r1 + p2[i] * (1 - r1))
        offspring_value2 = round(p1[i] * r2 + p2[i] * (1 - r2))
        offspring1.append(offspring_value1)
        offspring2.append(offspring_value2)

    return [offspring1, offspring2]


def fitness_dependent_xo(parent1, parent2, xo_op=uniform_xo, iterations=10):
    """Applies a chosen crossover operator xo_op  n times and selects the two best offspring based on fitness

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.
        xo_op (function, optional): Crossover operation. Defaults to uniform_xo.
        iterations (int, optional): Number of iterations. Defaults to 10.

    Returns:
        Individuals: Two offspring (highest fitness of the 10 generated), resulting from the crossover.
    """
    individuals = []
    for _ in range(iterations):
        offspring1, offspring2 = xo_op(parent1, parent2)
        individuals.append([offspring1, Individual(offspring1).get_fitness()])
        individuals.append([offspring2, Individual(offspring2).get_fitness()])

    sorted_individuals = sorted(individuals, key=lambda x: x[1])
    return sorted_individuals[0][0], sorted_individuals[1][0]


if __name__ == "__main__":
    # p1, p2 = [9,8,2,1,7,4,5,10,6,3], [1,2,3,4,5,6,7,8,9,10]
    # p1, p2 = [2,7,4,3,1,5,6,9,8], [1,2,3,4,5,6,7,8,9]
    p1, p2 = [9, 8, 4, 5, 6, 7, 1, 3, 2, 10], [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]
    o1, o2 = k_point_xo(p1, p2)
    print(o1, o2)
