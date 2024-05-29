from data.data_prep import nutrients, prices, target_nutrients
import numpy as np


# Penalty = Difference between sums of nutrients (includes excess and shortage of nutrients)
def fitness_sum_excess_shortfall(self):
    total_cost = np.dot(self.representation, prices)
    self.total_nutrients = np.dot(self.representation, nutrients)
    fitness = total_cost

    nutrient_shortfall = np.sum(target_nutrients) - np.sum(self.total_nutrients)
    fitness += abs(nutrient_shortfall) * 1000

    return fitness


# Penalty = Difference between sums of nutrients (Only nutrient shortage)
def fitness_sum_shortfall(self):
    total_cost = np.dot(self.representation, prices)
    self.total_nutrients = np.dot(self.representation, nutrients)
    fitness = total_cost

    nutrient_shortfall = np.maximum(
        np.sum(target_nutrients) - np.sum(self.total_nutrients), 0
    )
    fitness += nutrient_shortfall * 1000

    return fitness


# Penalty - Adds penalty for EACH nutrient shortage
def fitness_each_shortfall(self):
    total_cost = np.dot(self.representation, prices)
    self.total_nutrients = np.dot(self.representation, nutrients)
    fitness = total_cost

    for target_nutrient, current_nutrient in zip(
        target_nutrients, self.total_nutrients.tolist()
    ):
        if target_nutrient > current_nutrient:
            fitness += abs(target_nutrient - current_nutrient) * 1000

    return fitness


# Penalty - Adds penalty for EACH nutrient shortage and excess
def fitness_each_excess_shortfall(self):
    total_cost = np.dot(self.representation, prices)
    self.total_nutrients = np.dot(self.representation, nutrients)
    fitness = total_cost

    for target_nutrient, current_nutrient in zip(
        target_nutrients, self.total_nutrients.tolist()
    ):
        if target_nutrient != current_nutrient:
            fitness += abs(target_nutrient - current_nutrient) * 1000

    return fitness


# Penalty - Adds penalty for EACH nutrient shortage and excess with different weights(shortage x2, excess x1)
def fitness_each_excess_shortfall_weighted(self):
    total_cost = np.dot(self.representation, prices)
    self.total_nutrients = np.dot(self.representation, nutrients)
    fitness = total_cost

    for target_nutrient, current_nutrient in zip(
        target_nutrients, self.total_nutrients.tolist()
    ):
        if target_nutrient > current_nutrient:
            fitness += abs(target_nutrient - current_nutrient) * 2000
        if target_nutrient < current_nutrient:
            fitness += abs(target_nutrient - current_nutrient) * 1000

    return fitness
