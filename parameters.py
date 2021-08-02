# -*- coding: utf-8 -*-
import random
import numpy as np
import copy
import configparser


def set_parameter_limits_from_ini_file(file_name: str):
    if file_name == None:
        return
    config = configparser.ConfigParser(allow_no_value=False, strict=True, empty_lines_in_values=False,
                                       interpolation=None)
    config.read(file_name)
    if not config.has_section('parameter_info'):
        raise ValueError("Parameter info file has to start with a section name: parameter_info.")
    ParameterSet.XMIN = config.getint('parameter_info', 'XMIN')
    ParameterSet.XMAX = config.getint('parameter_info', 'XMAX')
    ParameterSet.XSTEP = config.getint('parameter_info', 'XSTEP')
    ParameterSet.YMIN = config.getint('parameter_info', 'YMIN')
    ParameterSet.YMAX = config.getint('parameter_info', 'YMAX')
    ParameterSet.YSTEP = config.getint('parameter_info', 'YSTEP')
    ParameterSet.DMIN = config.getint('parameter_info', 'DMIN')
    ParameterSet.DMAX = config.getint('parameter_info', 'DMAX')
    ParameterSet.DSTEP = config.getint('parameter_info', 'DSTEP')
    ParameterSet.PWMIN = config.getint('parameter_info', 'PWMIN')
    ParameterSet.PWMAX = config.getint('parameter_info', 'PWMAX')
    ParameterSet.PWSTEP = config.getint('parameter_info', 'PWSTEP')
    ParameterSet.IMIN = config.getint('parameter_info', 'IMIN')
    ParameterSet.IMAX = config.getint('parameter_info', 'IMAX')
    ParameterSet.ISTEP = config.getint('parameter_info', 'ISTEP')


class ParameterSet:
    """
    Class that represents the set of parameters for the LFI attack.
    """

    XMIN = 0
    XMAX = 100
    XSTEP = 5
    YMIN = 0
    YMAX = 100
    YSTEP = 5
    DMIN = 1
    DMAX = 100
    DSTEP = 10
    PWMIN = 1
    PWMAX = 100
    PWSTEP = 5
    IMIN = 0
    IMAX = 100
    ISTEP = 1

    def __init__(self, x=None, y=None, delay=None, power_width=None, intensity=None):
        limits = ParameterSet.get_param_limits(for_expanding=True, as_dict=True)
        self.x = random.randrange(*limits['x']) if x is None else x
        self.y = random.randrange(*limits['y']) if y is None else y
        self.delay = random.randrange(*limits['delay']) if delay is None else delay
        self.power_width = random.randrange(*limits['power_width']) if power_width is None else power_width
        self.intensity = random.randrange(*limits['intensity']) if intensity is None else intensity
        self.fitness = None
        self.fault_class = None
        self.created = 'i'

    @staticmethod
    def get_parameterset_from_indexes(indexes, levels):
        if len(indexes) != len(levels):
            raise ValueError()

        limits = ParameterSet.get_param_limits(for_expanding=True)
        if len(indexes) != len(limits):
            raise ValueError("To many indexes for creating parameter set. Parameter set has", len(limits),
                             "parameters.")

        ps = []
        for i in range(0, len(indexes)):
            parts = levels[i]
            values = np.arange(*limits[i])
            index = indexes[i]
            part = round(len(values) / parts, 0)
            ps.append(values[random.randrange(index * part, (index + 1) * part if index < parts - 1 else len(values))])
        return ParameterSet(*tuple(ps))

    @staticmethod
    def get_parameterset_from_uniform(array):
        if len(array) != 5:  # number of parameters
            raise ValueError()
        limits = ParameterSet.get_param_limits(for_expanding=True)
        ps = []
        for i in range(0, len(array)):
            values = np.arange(*limits[i])
            index = int(np.round(array[i] * (len(values) - 1), 0))
            ps.append(values[index])
        return ParameterSet(*tuple(ps))

    @staticmethod
    def get_param_limits(for_expanding=False, as_dict=False):
        if for_expanding:
            limits = [[ParameterSet.XMIN, ParameterSet.XMAX + ParameterSet.XSTEP, ParameterSet.XSTEP],
                      [ParameterSet.YMIN, ParameterSet.YMAX + ParameterSet.YSTEP, ParameterSet.YSTEP],
                      [ParameterSet.DMIN, ParameterSet.DMAX + ParameterSet.DSTEP, ParameterSet.DSTEP],
                      [ParameterSet.PWMIN, ParameterSet.PWMAX + ParameterSet.PWSTEP, ParameterSet.PWSTEP],
                      [ParameterSet.IMIN, ParameterSet.IMAX + ParameterSet.ISTEP, ParameterSet.ISTEP]]
        else:
            limits = [[ParameterSet.XMIN, ParameterSet.XMAX, ParameterSet.XSTEP],
                      [ParameterSet.YMIN, ParameterSet.YMAX, ParameterSet.YSTEP],
                      [ParameterSet.DMIN, ParameterSet.DMAX, ParameterSet.DSTEP],
                      [ParameterSet.PWMIN, ParameterSet.PWMAX, ParameterSet.PWSTEP],
                      [ParameterSet.IMIN, ParameterSet.IMAX, ParameterSet.ISTEP]]
        if as_dict:
            return {'x': limits[0], 'y': limits[1], 'delay': limits[2],
                    'power_width': limits[3], 'intensity': limits[4]}
        return limits

    @staticmethod
    def get_param_names():
        """
        Function returns parameter names from the ParameterSet solution.
        :param s: ParameterSet solution
        :return: list of parameter names of the ParameterSet
        """
        # ps = copy.deepcopy(self)
        # params = vars(ps)
        # params.pop('fitness', None)
        # params.pop('fault_class', None)
        # params.pop('created', None)
        return ['x', 'y', 'delay', 'power_width', 'intensity']

    @staticmethod
    def get_parameter_number():
        return 5

    @staticmethod
    def clip(parameter, value):
        """
        Function that clips the value of parameter to its min or max value if the value is not in the range.
        :param parameter: parameter name: string
        :param value: new value that can be out of rande: float or int
        :return: clipped value of the parameter
        """
        if parameter == 'x':
            return np.clip(value, ParameterSet.XMIN, ParameterSet.XMAX)
        if parameter == 'y':
            return np.clip(value, ParameterSet.YMIN, ParameterSet.YMAX)
        if parameter == 'delay':
            return np.clip(value, ParameterSet.DMIN, ParameterSet.DMAX)
        if parameter == 'power_width':
            return int(np.clip(value, ParameterSet.PWMIN, ParameterSet.PWMAX))
        if parameter == 'intensity':
            return int(np.clip(value, ParameterSet.IMIN, ParameterSet.IMAX))

    def update_fitness(self, fitness=None, fault_class: str = None):
        """
        Function updates fitness value and fault class. If sent without arguments, default values are used to
        reset the fitness value and fault class to None.
        :param fitness: fitness value or None for reset
        :param fault_class: fault class (string) or None for reset
        :return: No return value, the object is updated
        """
        self.fitness = fitness
        self.fault_class = fault_class

    def update(self, key, value, reset_fitness=True):
        """
        Function that updates the parameter 'key' with value 'value'.
        This function resets the fitness value and fault class, unless the last argument 'reset_fitness' is set to False.
        If 'reset_fitness' is False, the fitness will not change, it is expected from the user to know what the are doing,
        and that the fitness might be invalid.
        :param key: parameter name
        :param value: new value to update the parameter
        :param reset_fitness: bool value for resetting fitness. Default is True.
        :return: No return value, the object is updated
        """
        if key == 'x':
            self.x = np.clip(value, ParameterSet.XMIN, ParameterSet.XMAX)
        elif key == 'y':
            self.y = np.clip(value, ParameterSet.YMIN, ParameterSet.YMAX)
        elif key == 'delay':
            self.delay = np.clip(value, ParameterSet.DMIN, ParameterSet.DMAX)
        elif key == 'power_width':
            self.power_width = int(np.clip(value, ParameterSet.PWMIN, ParameterSet.PWMAX))
        elif key == 'intensity':
            self.intensity = int(np.clip(value, ParameterSet.IMIN, ParameterSet.IMAX))
        if not reset_fitness:
            return
        self.fitness = None
        self.fault_class = None

    def __str__(self):
        return f"{self.created} (x={self.x}, y={self.y}, delay={self.delay}, " \
               f"power width={self.power_width}, intensity={self.intensity}, fitness={self.fitness}, fault class={self.fault_class})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """
        Equal operator.
        :param other: ParameterSet object
        :return: True if all parameter values are the same with the other object, False otherwise.
        """
        if not np.isclose(self.x, other.x):
            return False
        if not np.isclose(self.y, other.y):
            return False
        if not np.isclose(self.delay, other.delay):
            return False
        if not np.isclose(self.power_width, other.power_width):
            return False
        if not np.isclose(self.intensity, other.intensity):
            return False
        return True

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.x, self.y, self.delay, self.power_width, self.intensity))

    def __sub__(self, other):
        """
        Subtraction of two ParameterSet objects.
        Subtract other from this object. All parameter values are subtracted with the value of the same parameter
        of the other object. The values are clipped. This also resets the fitness.
        :param other: ParameterSet object
        :return: updated self
        """
        if type(self) != type(other):
            raise NotImplemented
        ps = ParameterSet()
        ps.x = np.clip(self.x - other.x, ParameterSet.XMIN, ParameterSet.XMAX)
        ps.y = np.clip(self.y - other.y, ParameterSet.YMIN, ParameterSet.YMAX)
        ps.delay = np.clip(self.delay - other.delay, ParameterSet.DMIN, ParameterSet.DMAX)
        ps.power_width = int(np.clip(self.power_width - other.power_width, ParameterSet.PWMIN, ParameterSet.PWMAX))
        ps.intensity = int(np.clip(self.intensity - other.power_width, ParameterSet.IMIN, ParameterSet.IMAX))
        ps.fitness = None
        ps.fault_class = None
        return ps

    def __mul__(self, other):
        """
        Multiplication of two ParameterSet objects.
        Multiply self parameter values with the same paramter values from the other object.
        The values are clipped after multiplication. This also resets the fitness.
        :param other: ParameterSet object
        :return: updated self
        """
        if type(self) != type(other):
            raise NotImplemented
        ps = ParameterSet()
        ps.x = np.clip(self.x * other.x, ParameterSet.XMIN, ParameterSet.XMAX)
        ps.y = np.clip(self.y * other.y, ParameterSet.YMIN, ParameterSet.YMAX)
        ps.delay = np.clip(self.delay * other.delay, ParameterSet.DMIN, ParameterSet.DMAX)
        ps.power_width = int(np.clip(self.power_width * other.power_width, ParameterSet.PWMIN, ParameterSet.PWMAX))
        ps.intensity = int(np.clip(self.intensity * other.power_width, ParameterSet.IMIN, ParameterSet.IMAX))
        ps.fitness = None
        ps.fault_class = None
        return ps

    def __rmul__(self, other):
        """
        Reverse multiplication for multiplication with numbers instead of ParameterSet objects.
        When multiplying with number, it should be, e.g., 2 * ParameterSet_object, and not
        ParameterSet_object * 2. It multiplies all parameter values with the sent number.
        This also resets the fitness.
        :param other: float or int
        :return: updated self
        """
        if type(other) not in [float, int]:
            raise NotImplemented
        ps = ParameterSet()
        ps.x = np.clip(self.x * other, ParameterSet.XMIN, ParameterSet.XMAX)
        ps.y = np.clip(self.y * other, ParameterSet.YMIN, ParameterSet.YMAX)
        ps.delay = np.clip(self.delay * other, ParameterSet.DMIN, ParameterSet.DMAX)
        ps.power_width = int(np.clip(self.power_width * other, ParameterSet.PWMIN, ParameterSet.PWMAX))
        ps.intensity = int(np.clip(self.intensity * other, ParameterSet.IMIN, ParameterSet.IMAX))
        ps.fitness = None
        ps.fault_class = None
        return ps
