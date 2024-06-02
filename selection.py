from operator import attrgetter
from random import uniform, choice, choices


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    if population.optim == "max":
        total_fitness = sum([i.fitness for i in population])
        r = uniform(0, total_fitness)
        position = 0
        for individual in population:
            position += individual.fitness
            if position > r:
                return individual
    elif population.optim == "min":
        # Invert fitness values for "min" optimization
        inverted_fitness = [1 / i.fitness for i in population]
        total_inverted_fitness = sum(inverted_fitness)
        r = uniform(0, total_inverted_fitness)
        position = 0
        for individual, inverted_value in zip(population, inverted_fitness):
            position += inverted_value
            if position > r:
                return individual
    else:
        raise Exception(f"Optimization not specified (max/min)")


def tournament_sel(population, tour_size=3):
    """Randomly chooses n individuals from the population and selects the best individual based on fitness.
    Tournament size can be specified.

    Args:
        population (Population): The population we want to select from.
        tour_size: The size of the tournament, that is the number of individuals chosen from the population. Defaults to 3.

    Returns:
        Individual: selected individual with the best fitness.
    """
    tournament = [choice(population) for _ in range(tour_size)]
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))


def rank_sel(population):
    """Begins by sorting the population based on fitness in descending order,
    assigns selection probabilities proportional to the rank of each individual's fitness, and selects an individual based on these probabilities.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    if population.optim == "min":
        sorted_pop = sorted(population, key=attrgetter("fitness"), reverse=True)
        sel_probs = [
            rank / sum(range(len(sorted_pop)))
            for rank, fitness in enumerate(sorted_pop, start=1)
        ]
        return choices(sorted_pop, sel_probs)[0]
    if population.optim == "max":
        raise Exception(f"Optimization not specified for Maximization")
    else:
        raise Exception(f"Optimization not specified (max/min)")
