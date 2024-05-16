from operator import attrgetter
from random import uniform, choice


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
    tournament = [choice(population) for _ in range(tour_size)]
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))
