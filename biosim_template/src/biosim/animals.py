"""
Animals class for biosim
"""

import random as rd
import math as m
rd.seed(12345)
"""
Class describing hebrivores

:param 
"""


class Herbivore:
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

    def __init__(self,age, weight, fitness=None):
        """
        :param age: the age of the animal
        :param weight: the weight of the animal
        :param fitness: the fitness of the animal
        """

        self.age = age
        self.weight = weight
        self.fitness = fitness

    def __repr__(self):
        return f'Herbivore(age:{self.age}, Weight:{self.weight})'

    #@classmethod?
    def calculate_fitness(self):
        """
        Calculates the fitness of the animal by using the fitness formula given in the task
        """

        if self.weight <= 0:
            self.fitness = 0
        else:
            q_plus = 1/(1 + m.exp(self.params['phi_age']*(self.age - self.params['a_half'])))
            q_minus = 1/(1 + m.exp(self.params['phi_weight']*(self.weight - self.params['w_half'])))
            self.fitness = q_plus*q_minus


    def grow_one_year(self):
        """
        Makes the animal a year older
        """
        self.age += 1


    def weight_gained_from_eating(self, fodder):
        """
        Calculates the gain of weigth by an animal eating
        :param fodder: food accsessable to the animal
        """

        self.weight += fodder * self.params['beta']


    def lose_weight(self):
        """
        Calulates the loss of weight of an animal
        :return:
        """

        self.weight -= self.weight*self.params['mu']


    def migrate(self):
        pass


    def death(self):
        """
        calculates if animal dies using fitness omega.
        :return: returns 1 if the animal dies and 0 if it lives
        """
        p = rd.random()
        if self.weight == 0:
            return True
        else:
            prob_death = self.params['omega'] * (1 - self.fitness)
            if  p < prob_death:
                return True


    def lose_weight_birth(self, w_child):
        """
        Calculates the weight the "Mother" loses to birth
        :param w_child: weight of the child born

        """
        return w_child * self.params['xi']


    def birth(self,N):
        """
        calculates the probabillity for
        :param N: is the number of animals in the cell
        """
        w_child = rd.gauss(self.params['w_birth'],self.params['sigma_birth'])
        if self.lose_weigt_birth(w_child) <= self.weight:
            if rd.random() < min([1, self.params['gamma'] * self.params['phi'] *(N - 1)]):
                self.weight -= self.lose_weight_birth(w_child)
                return Herbivore(1,w_child)
            else:
                return False
        else:
            return False








