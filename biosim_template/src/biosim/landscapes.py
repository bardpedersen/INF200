import numpy as np
from biosim.animals import Herbivore




class LowLand:
    def __init__(self):
        self.fodder = 0
        self.population_herb = []
        self.population_sum = None


    def add_population(self,population=None):
        """
        adds a population to the lanscape location, and turns it in to an animal object
        :param population: the population to add to the map
        :return:
        """

        for animal in population:
            if animal['species'] == 'Herbivore':
                self.population_herb.append(Herbivore(animal['age'], animal['weight']))

    def sum_of_herbivores(self):
        self.population_sum = len(self.population_herb)

    def calculate_fitness_in_cell(self):
        """
        uses the calculate fitness function from animals
        to calculate the fitness of each animal in cell
        :return:
        """

        for animal in self.population_herb:
            animal.calculate_fitness()

    def add_fooder(self):
        self.fodder = 800

    def feeding(self):
        """
        Animals residing in a cell eat in descend- ing order of fitness.
        Each animal tries every year to eat an amount F of fodder,
        but how much feed the animal obtain depends on fodder available in the cell
        this function also sets the fooder for

        Here:
        F = 10
        f_max = 800
        """
        
        for animal in self.population_herb:
            self.population_herb.sort(key=lambda animal: animal.fitness, reverse=True)
            appetite = 10
            if self.fodder == 0:
                break
            elif self.fodder >= appetite:
                animal.weight_gained_from_eating(appetite)
                self.fodder = self.fodder - appetite
            elif 0 < self.fodder < appetite:
                animal.weight_gained_from_eating(self.fodder)
                self.fodder = 0


    def procreation_in_cell(self):
        """
        Animals can mate if there are at least two animals of the same species in a cell.
        Gender plays no role in mating.Each animal can give birth to at most one off- spring per year.
        At birth, the mother animal loses ξ times the actual birth weight of the baby.
        If the mother would lose more than her own weight,
        then no baby is born and the weight of the mother remains unchanged.
        """
        new_borns = []
        N = self.population_sum
        for animal in self.population_herb:
            new_born = animal.birth(N)
            if new_born is not False:
                new_borns.append(new_born)
            N -= 1
        self.population_herb += new_borns #adds the newborns to the population at the end



    def migration(self):
        """No migration on one cell island"""
        pass


    def aging_in_cell(self):
        """
        At birth, each animal has age a = 0 .
        Age increases by one year for each year that passes
        """
        for animal in self.population_herb:
            animal.grow_one_year()


    def weight_lost_in_cell(self):
        """
        Every year, the weight of the animal decreases.
        """
        for animal in self.population_herb:
            animal.lose_weight()


    def death_in_cell(self):
        """
        Animals die when its weight is w = 0 or
        by probability
        """
        for animal in self.population_herb:
            if animal.death():
                self.population_herb.pop(animal)



class Water:
    def __init__(self):
        self._fodder = 0






