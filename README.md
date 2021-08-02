
# On the Importance of Initial Solutions Selection in Fault Injection

### Authors:
##### Marina Krček and Daniele Fronte and Stjepan Picek

Implementation of work reported in paper  *On the Importance of Initial Solutions Selection in Fault Injection*.


### Running
Python 3 should be used, and libraries from *requirements.txt* should be installed. Newer versions can be used, but if there are some issues, one can try with the older versions defined in the *requirements.txt*.
Then, simply running *main.py* should work. *main.py* is a script that shows how to use the implementation of the Genetic Algorithm.
There is also *main_random.py*, which shows the random search we used in the paper.


### Implementation in *main.py*
Firstly, we need to import the *ga* module with the implementation of the *GeneticAlgorithm* class. We also need to import the *fitness* module for the calculation of the fitness value for fault classes received from the injection.
```python
import ga
import fitness
```
Then, we need to create an instance of the *GeneticAlgorithm* class using its constructor.
To create an instance of the *GeneticAlgorithm* class certain parameters need to be sent to the constructor of the class.
The parameters are:
  - **apply_on_bench_function**: function that applies the bench parameters and executes the laser shot and returns the response fault class (id),
  - **carto_set_iteration**: function that takes the GA iteration number and sets it internally (needed for logging in our setup),
  - **pop_size**: population size, default: 30,
  - **mutation_probability**: mutation probability, default: 0.05,
  - **elite_size**: elite size, default: 2,
  - **nb_measurements**: number of laser shots with the same parameters (same spot), default: 5,
  - **max_iterations**: maximum number of iterations for the memetic algorithm, default: 50,
  - **parameter_info_file**: file with parameter bounds, default: None,
  - **initialization_function**: Initialization function, default: random_initialization,
  - **stop_condition**: function that checks the condition for terminating the algorithm, default: stop_cond_iterations,  
  - **sort_function**: Sort function, default: xy_snake_sort,
  - **selection**: selection operator, default: roulette_wheel,
  - **crossover**: crossover operator, default: uniform_crossover,
  - **mutation**: mutation operator, default: uniform_mutation,
  - **local_search**: function performing local search, default: hooke_jeeves,
  - **fitness_func**: function for calculating the fitness of the solutions, default: percentage_fitness.


From the list of these fault classes, the user has to call one fitness function from the *fitness* package. Possible fitness functions are 
- fitness: from Maldini et al.
- percentage_fitness: calculates the fitness based on the percentage of the fault classes in the number-of-measurements injections.


## Additional notes

The population is a list of ParameterSet class instances, and below you can see an example. 
However, the values are in the class, not as a tuple. \
[\
(x1, y1, delay1, power_width1, intensity1, fitness1, fault_class1), \
(x2, y2, delay2, power_width2, intensity2, fitness2, fault_class2), \
(x3, y3, delay3, power_width3, intensity3, fitness3, fault_class3), \
(x4, y4, delay4, power_width4, intensity4, fitness4, fault_class4), \
... \
]



Additionally, what is also important is to set limits and allowed intervals for parameter values so that the genetic algorithm can create valid parameter sets for the laser bench and device under test.

The user can create a file similar to file *parameter_info.ini* using a section **parameter_info** in the .ini configuration file.
The name of the file created by the user should be set as an argument to the GeneticAlgorithm class constructor.
```buildoutcfg
[parameter_info]
XMIN = 0
XMAX = 100
XSTEP = 1
YMIN = 0
YMAX = 100
YSTEP = 1
DMIN = 0
DMAX = 100
DSTEP = 1
PWMIN = 0
PWMAX = 100
PWSTEP = 1
IMIN = 0
IMAX = 100
ISTEP = 1
```

Additionally, the user can also create a file that defines the fault class names, ids, and fitness values.
An example of such a file is the *fitness.info* file. Lines starting with `#` are ignored.
The format should be as shown below. So, there are three columns, the first one has the id, the second column is the name, and the last column is the fitness value.
It is important to say that, since we run the shots multiple times with the same parameters, it could be that the response is several different fault classes. In that case, the fault class will be called `changing`, and the fitness value of that class depends on the fitness function selected by the user in the source code.
```buildoutcfg
#id name fitness
2 fail 10
1 mute 5
0 pass 2
```

