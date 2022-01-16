"""
Animals class for biosim
"""

import random as rd
import math as m

"""
Class describing Animals 

:param 
"""


class Animal:
    def __init__(self, age, weight):
        """
        initiates instance of animal

        :param age: the age of the animal
        :param weight: the weight of the animal
        """
        if age is None:
            age = 0
        elif age < 0:
            raise ValueError('Age has to be a positive integr')
        self.age = age
        if weight is None:
            weight = 0
        elif weight < 0:
            raise ValueError('Weight has to be positive interg or zero')
        self.weight = weight
        self.fitness = None
        self.has_migrated = False
        self.is_dead = False

    def set_params(cls, params):
        """
        takes an dictionatry of parameters and replaces default params

        :param: params: a dictionary with parameter values
        """
        for parameter in params:
            if parameter in cls.params:
                if params[parameter] < 0:
                    raise ValueError(f'{parameter} has to be positive, cant be {params[parameter]}')
                if parameter == 'eta' and params[parameter] > 1:
                    raise ValueError(f'eta has to be smaller than 1 cant be {params[parameter]}')
                if parameter == 'DeltaPhiMax' and params[parameter] == 0:
                    raise ValueError(f'DeltaPhiMax must be nonzero positive, cannot be {params[parameter]}')
                else:
                    cls.params[parameter] = params[parameter]
            else:
                raise KeyError(f'{parameter} is not a accepted parameter')

    def calculate_fitness(self):
        """
        Calculates the fitness of the animal by using the fitness formula given in the task
        """

        if self.weight <= 0:
            self.fitness = 0
        else:
            q_plus = 1/(1 + m.exp(self.params['phi_age']*(self.age - self.params['a_half'])))
            q_minus = 1/(1 + m.exp(-self.params['phi_weight']*(self.weight - self.params['w_half'])))
            self.fitness = q_plus*q_minus

    def grow_one_year(self):
        """
        Makes the animal a year older
        """
        self.age += 1

    def weight_gained_from_eating(self, fodder):
        """
        Calculates the gain of weight by an animal eating
        :param fodder: food accsessable to the animal
        """

        self.weight += fodder * self.params['beta']

    def lose_weight(self):
        """
        Calulates the loss of weight of an animal
        :return:
        """

        self.weight -= self.weight*self.params['eta']
        if self.weight < 0:
            self.weight = 0

    def death(self):
        """
        calculates if animal dies using fitness omega.
        :return: returns 1 if the animal dies and 0 if it lives
        """
        p = rd.random()
        self.calculate_fitness()
        prob_death = self.params['omega'] * (1 - self.fitness)
        if self.weight == 0 or p < prob_death:
            self.is_dead = True

    def migrate(self):
        if not self.has_migrated:
            self.calculate_fitness()
            move_prob = self.params['mu'] * self.fitness
            p = rd.random()
            if p < move_prob:
                self.has_migrated = True
        else:
            self.has_migrated = False

    def birth(self, N, species='herb'):
        """
        calculates the probabillity for birth of animals and returns a animal


        :param N: is the number of animals in the cell
        :param species: selects what kind of animal to return, default is Herbivore
        """

        w_child = rd.gauss(self.params['w_birth'], self.params['sigma_birth'])
        lost_weight = w_child*self.params['xi']
        zero_conditon = self.params['zeta']*(self.params['w_birth']+self.params['sigma_birth'])
        if self.weight < lost_weight:
            return None
        elif w_child <= 0:
            return None
        elif self.weight < zero_conditon:
            return None
        else:
            p = rd.random()
            p_birth = min(1, self.params['gamma']*self.fitness*(N-1))
            if p < p_birth:
                self.weight -= lost_weight
                if species == 'herb':
                    return Herbivore(0, w_child)
                elif species == 'carn':
                    return Carnivore(0, w_child)


class Herbivore(Animal):
    """
    class containing animals of species herbivores
    the params dictionary contains all the "static" parameters of the species
    """

    params = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40.0,
        'phi_age': 0.6,
        'w_half': 10.0,
        'phi_weight': 0.1,
        'mu': 0.25,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10
        }

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)

    def __repr__(self):
        return f'Herbivore, (age:{self.age}, Weight:{self.weight}, Is_dead: {self.is_dead}, ' \
               f'Has_migrated: {self.has_migrated})'


class Carnivore(Animal):
    params = {
        'w_birth': 6.0,
        'sigma_birth': 1.0,
        'beta': 0.75,
        'eta': 0.125,
        'a_half': 40.0,
        'phi_age': 0.3,
        'w_half': 4.0,
        'phi_weight': 0.4,
        'mu': 0.4,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.8,
        'F': 50,
        'DeltaPhiMax': 10
    }

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)

    def __repr__(self):
        return f'Carnivore, (age:{self.age}, Weight:{self.weight}, Is_dead: {self.is_dead}, ' \
               f'Has_migrated: {self.has_migrated})'

    def carnivore_kill_prob(self, prey):
        """
        Calulates the probabillity if carnivore kills herbivore

        """

        difference_fitness = self.fitness - prey.fitness
        if self.fitness < prey.fitness:
            prob = 0
        elif 0 < difference_fitness < self.params['DeltaPhiMax']:
            prob = difference_fitness/self.params['DeltaPhiMax']
        else:
            prob = 1

        return prob


if __name__ == '__main__':
    for _ in range(100):
        print(rd.random())
