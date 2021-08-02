from parameters import *
import random

# MutationFunction = Callable[[ParameterSet, float], ParameterSet]


def uniform_mutation(solution: ParameterSet, mutation_prob=0.05):
    """
    Function takes a ParameterSet solution and changes some of the parameter values with probability
    self.mutation_prob. The values are replaced by the new random value (mutation) from the allowed interval
    for the given parameter.
    :param mutation_prob:
    :param solution: ParameterSet solution
    :return: ParameterSet solution after mutation
    """
    # uniform, operator replaces the value of the chosen gene with a uniform random value selected between the user-specified upper and lower bounds for that gene.
    rand = random.random
    limits = ParameterSet.get_param_limits(for_expanding=True, as_dict=True)
    if rand() < mutation_prob: solution.x = random.randrange(*limits['x'])
    if rand() < mutation_prob: solution.y = random.randrange(*limits['y'])
    if rand() < mutation_prob: solution.delay = random.randrange(*limits['delay'])
    if rand() < mutation_prob: solution.power_width = random.randrange(*limits['power_width'])
    if rand() < mutation_prob: solution.intensity = random.randrange(*limits['intensity'])
    return solution