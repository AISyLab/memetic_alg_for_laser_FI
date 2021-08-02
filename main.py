import ga
import collections
import json
import numpy as np
from initializations import TaguchiInitialization, taguchi_from_example, taguchi_from_file
import fitness
from helper import converter
from sort_algorithms import greedy_euclidean
from crossovers import uniform_crossover, average_crossover
from bench_connection import dummy_cartography
from selections import ktournament
import copy
from stop_conditions import *

########## GENETIC ALGORITHM PARAMETERS ###########
POPULATION_SIZE = 36
ITERATIONS = 50
MUTATION_PROB = 0.05  # mutation probability
ELITE_SIZE = 2

########## FAULT INJECTION PARAMETERS ############
NB_MEASUREMENTS = 5  # with the same parameter set (same spot)
parameter_info_file = 'parameter_info.ini'


def dummy_set_iteration(n):
    iter = n
    return iter


if __name__ == "__main__":
    fitness.set_fitness_values('fitness.info')

    # run_times defines how many times you want to run the same GA
    run_times = 1
    
    # construct the cartography class
    carto = dummy_cartography()
    
    # create the genetic algorithm instance 
    # (define the parameters and functions of the GA)
    # GA class takes the apply_bench_parameter function of the cartography class
    gen_alg = ga.GeneticAlgorithm(carto.apply_bench_parameter,
                                  dummy_set_iteration,
                                  nb_measurements=NB_MEASUREMENTS,
                                  max_iterations=ITERATIONS,
                                  pop_size=POPULATION_SIZE, 
                                  mutation_probability=MUTATION_PROB, 
                                  elite_size=ELITE_SIZE,  
                                  parameter_info_file=parameter_info_file,
                                  stop_condition=stop_cond_iterations,
                                  selection=ktournament(),
                                  crossover=average_crossover,
                                  sort_function=greedy_euclidean)
    
    # print information about the GA
    print(gen_alg)
    
    for i in range(run_times):
        print("Running GA ", i + 1)
        
        # initialization, evolution through iterations and local search
        # done in the GeneticAlgorithm::run function
        population = gen_alg.run()
        print(population)
