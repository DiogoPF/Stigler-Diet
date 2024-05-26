from random import randint, sample, uniform, random, randrange
import copy


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


def k_point_xo(parent1, parent2, k=3):
    """Implementation of n-point crossover.

    Args:
        parent1 (list of int): First parent for crossover.
        parent2 (list of int): Second parent for crossover.

    Returns:
        tuple: Two offspring, resulting from the crossover.
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

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

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
    """Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_points = sample(range(len(parent1)), 2)
    xo_points.sort()

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
    offspring = [int(parent1[i] + parent2[i] / 2) for i in range(len(parent1))]
    return offspring


def cycle_xo(p1, p2):
    """Implementation of cycle crossover for lists of integers with non-unique values.

    Args:
        p1 (list): First parent for crossover (list of integers).
        p2 (list): Second parent for crossover (list of integers).

    Returns:
        list: Two offspring, resulting from the crossover.
    """
    # Offspring placeholders
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)

    # Convert parents to dictionaries of index:value
    p1_dict = {i: p1[i] for i in range(len(p1))}
    p2_dict = {i: p2[i] for i in range(len(p2))}

    while None in offspring1:
        index = offspring1.index(None)
        val1 = p1_dict[index]
        val2 = p2_dict[index]

        # Copy the cycle elements
        while val1 != val2:
            offspring1[index] = p1_dict[index]
            offspring2[index] = p2_dict[index]
            val2 = p2_dict[index]
            index = list(p1_dict.keys()).index(val2)

        # Copy the rest
        for i in range(len(offspring1)):
            if offspring1[i] is None:
                offspring1[i] = p2_dict[i]
                offspring2[i] = p1_dict[i]

    return offspring1, offspring2


def int_arithmetic_crossover(p1, p2):
    """Implementation of integer arithmetic crossover.

    Args:
        p1 (list of int): First parent for crossover.
        p2 (list of int): Second parent for crossover.

    Returns:
        list of list of int: Two offspring resulting from the crossover.
    """
    offspring1 = []
    offspring2 = []

    for i in range(len(p1)):
        # Choose crossover points
        r1 = random()
        r2 = random()
        offspring_value1 = round(p1[i] * r1 + p2[i] * (1 - r1))
        offspring_value2 = round(p1[i] * r2 + p2[i] * (1 - r2))
        offspring1.append(offspring_value1)
        offspring2.append(offspring_value2)

    return [offspring1, offspring2]


if __name__ == "__main__":
    # p1, p2 = [9,8,2,1,7,4,5,10,6,3], [1,2,3,4,5,6,7,8,9,10]
    # p1, p2 = [2,7,4,3,1,5,6,9,8], [1,2,3,4,5,6,7,8,9]
    p1, p2 = [9, 8, 4, 5, 6, 7, 1, 3, 2, 10], [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]
    o1, o2 = pmx(p1, p2)
    print(o1, o2)


def reduce(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # offspring placeholders
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)

    while None in offspring1:
        index = offspring1.index(None)
        val1 = p1[index]
        val2 = p2[index]

        # copy the cycle elements
        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)

        # copy the rest
        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return offspring1, offspring2


def blend_crossover(parent1, parent2, alpha=0.3):
    offspring1 = []
    offspring2 = []

    for i in range(len(parent1)):
        min_val = min(parent1[i], parent2[i])
        max_val = max(parent1[i], parent2[i])
        range_val = max_val - min_val

        # Calculate the range around parents' genes
        min_range = min_val - alpha * range_val
        max_range = max_val + alpha * range_val

        # Generate offspring gene
        gene1 = round(uniform(min_range, max_range))
        gene2 = round(uniform(min_range, max_range))

        offspring1.append(gene1)
        offspring2.append(gene2)

    return offspring1, offspring2
