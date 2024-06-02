# Stigler’s Diet Problem: A Genetic Algorithm Approach

Computational Intelligence for Optimization  - Diogo Fernandes (20220507@novaims.unl.pt)

## Context

In 1945, “Stigler posed the following problem: For a moderately active man (economist) weighing 154 pounds, how much of each of 77 foods should be eaten on a daily basis so that the man’s intake of nine nutrients (including calories) will be at least equal to the recommended dietary allowances (RDAs) suggested by the National Research Council in 1943, with the cost of the diet being minimal?”. Being RDAs the levels of intake of essential nutrients deemed adequate to meet the known nutrient needs of  practically all healthy persons (Garille et all. ,2001).

## Aim

This project aims to develop a genetic algorithm that provides the optimal solution to the Stigler’s diet problem. Multiple genetic operators, algorithm parameters and fitness functions were tested to ensure the best possible result.



## Files Overview

- [Report](https://github.com/DiogoPF/Stigler-Diet/tree/main/Report/images) - Folder containing the report pdf file and all tables/visualizations extracted
- [Data](https://github.com/DiogoPF/Stigler-Diet/tree/main/data) - Folder containing the raw data file and data pre processing script.
- [Results](https://github.com/DiogoPF/Stigler-Diet/tree/main/results) - Folder containing csv files with run logs and Notebook of results exploration
- [aux_funcs](https://github.com/DiogoPF/Stigler-Diet/blob/main/aux_funcs.py) - Helper functions to run and log configurations
- [charles.py](https://github.com/DiogoPF/Stigler-Diet/blob/main/charles.py) - Individual and Population classes definition
- [fitness.py](https://github.com/DiogoPF/Stigler-Diet/blob/main/fitness.py) - Fitness functions definition
- [mutation.py](https://github.com/DiogoPF/Stigler-Diet/blob/main/mutation.py) - Mutation functions definition
- [selection.py](https://github.com/DiogoPF/Stigler-Diet/blob/main/selection.py) - Selection methods definition
- [stingler_diet.py](https://github.com/DiogoPF/Stigler-Diet/blob/main/stingler_diet.py) - Configurations tested
- [xo.py](https://github.com/DiogoPF/Stigler-Diet/blob/main/xo.py) - Crossover functions definition
