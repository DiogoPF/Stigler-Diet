from operator import attrgetter
from random import shuffle, choice, sample, random
from copy import copy
from data.data_prep import commodities, nutrients, target_nutrients
import numpy as np
from functools import partial


class Individual:
    # we always initialize
    def __init__(self, representation=None, size=None, valid_set=None, repetition=True):

        if representation is None:
            if repetition:
                # individual will be chosen from the valid_set with a specific size
                self.representation = [choice(valid_set) for i in range(size)]
            else:
                self.representation = sample(valid_set, size)

        # if we pass an argument like Individual(my_path)
        else:
            self.representation = representation

        # fitness will be assigned to the individual
        self.fitness = self.get_fitness()

    # methods for the class
    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness function.")

    def get_neighbours(self):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f" Fitness: {self.fitness}"

    def get_food_list(self):
        food_dict = {
            commodities[i]: self.representation[i]
            for i in range(len(self.representation))
            if self.representation[i] > 0
        }
        return food_dict

    def get_nutrients_diff(self):
        current_nutrients = np.dot(self.representation, nutrients)
        diff = current_nutrients - np.array(target_nutrients)
        return diff


class Population:
    def __init__(self, size, optim, **kwargs):

        # population size
        self.size = size

        # defining the optimization problem as a minimization or maximization problem
        self.optim = optim

        self.individuals = []

        # appending the population with individuals
        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs["sol_size"],
                    valid_set=kwargs["valid_set"],
                    repetition=kwargs["repetition"],
                )
            )

    def evolve(
        self,
        gens,
        xo_prob,
        mut_prob,
        select,
        xo,
        mutate,
        elitism,
        **kwargs,
    ):
        tour_size = kwargs.get("tour_size", False)
        max_tries = kwargs.get("max_tries", False)
        k_point = kwargs.get("k_point", False)
        uniform_prob = kwargs.get("uniform_prob", False)

        if tour_size and select.__name__ == "tournament_sel":
            select = partial(select, tour_size=tour_size)

        if max_tries and mutate.__name__ == "fitness_dependent_swap":
            mutate = partial(mutate, max_tries=max_tries)

        if k_point and xo.__name__ == "k_point_xo":
            xo = partial(xo, k=k_point)

        if uniform_prob and xo.__name__ == "uniform_xo":
            xo = partial(xo, prob=uniform_prob)

        fitness_gen = []
        # gens = 100
        for i in range(gens):
            new_pop = []

            if elitism:
                if self.optim == "max":
                    elite = copy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = copy(min(self.individuals, key=attrgetter("fitness")))

                # new_pop.append(elite)

            while len(new_pop) < self.size:
                try:
                    # selection
                    parent1, parent2 = select(self), select(self)
                    # xo with prob
                    if random() < xo_prob:
                        offspring1, offspring2 = xo(parent1, parent2)
                    # replication
                    else:
                        offspring1, offspring2 = parent1, parent2
                except ValueError:
                    parent1, parent2, parent3, parent4 = (
                        select(self),
                        select(self),
                        select(self),
                        select(self),
                    )
                    if random() < xo_prob:
                        offspring1 = xo(parent1, parent2)
                        offspring2 = xo(parent3, parent4)
                    else:
                        offspring1, offspring2 = parent1, parent2

                # mutation with prob
                if random() < mut_prob:
                    offspring1 = mutate(offspring1)
                if random() < mut_prob:
                    offspring2 = mutate(offspring2)

                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            if elitism:
                if self.optim == "max":
                    worst = min(new_pop, key=attrgetter("fitness"))
                    if elite.fitness > worst.fitness:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)
                if self.optim == "min":
                    worst = max(new_pop, key=attrgetter("fitness"))
                    if elite.fitness < worst.fitness:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)

            self.individuals = new_pop

            if self.optim == "max":
                best_individual = max(self, key=attrgetter("fitness"))
                print(f"Best individual of gen #{i + 1}: {best_individual}")
            elif self.optim == "min":
                gen = i + 1
                best_fitness = min(self, key=attrgetter("fitness"))
                fitness_gen.append([gen, best_fitness.fitness])
                best_individual = min(self, key=attrgetter("fitness"))
                print(f"Best individual of gen #{i + 1}: {best_individual}")
        print(best_individual.get_food_list())
        print(best_individual.get_nutrients_diff().tolist())
        return fitness_gen

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
