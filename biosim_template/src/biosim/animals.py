"""
Animals class for biosim
"""

import random as rd
import math as m
"""
Class describing hebrivores

:param 
"""
class Herbivore:

    params = {
        phi_age: 0.6,
        phi_weight: 0.1,
        a_half: 40.0,
        w_half = 10.0,
        beta = 0.9,
        mu = 0.25
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

    #@classmethod?
    def calculate_fitness(self):
        """
        Calculates the fitness of the animal by using the fitness formula given in the task
        """

        if self.weight <= 0:
            self.fitness = 0
        else:
            q_plus = 1/(1 + m*exp(self.params[phi_age]*(self.age -self.params[a_half])))
            q_minus =  1/(1 + m*exp(self.params[phi_weight]*(self.weight - self.params[w_half])))
            self.fitness = q_plus*q_minus

    def growing_up(self):
        """
        Makes the animal a year older
        """
        self.age += 1

    def feeding(self, fodder):
        """
        Calculates the gain of weigth by an animal eating
        :param fodder: food accsessable to the animal
        :return:
        """

        self.weight += fodder * self.params[beta]

    def lose_weigt(self):
        """
        Calulates the loss of weight of an animal
        :return:
        """

        self.weight -= self.weight*self.params[mu]






