from biosim.animals import Herbivore, Carnivore
from biosim.landscapes import LowLand, Water
from biosim.island_map import Map

import numpy as np
import matplotlib.pyplot as plt


class WindowPlot:
    def __init__(self, island_map):
        self.nr_herb = []
        self.nr_car = []
        self.weight_herb = []
        self.weight_car = []
        self.fitness_herb = []
        self.fitness_car = []
        self.age_herb = []
        self.age_car = []
        self.years = []
        self.island_map = island_map

    def update_years(self, year):
        self.years.append(year)

    def update_animals(self, num_animals_herb, num_animals_car):
        self.nr_herb.append(num_animals_herb)
        self.nr_car.append(num_animals_car)

    def update_animals_age(self):
        self.age_car.append()
        self.age_herb.append()
        pass

    def update_animals_fitness(self):
        self.fitness_car.append()
        self.fitness_herb.append()
        pass

    def update_animals_weight(self):
        self.weight_car.append()
        self.weight_herb.append()
        pass

    def make_graph(self):
        plt.plot(self.years, self.nr_herb)
        plt.xlabel('Years')
        plt.ylabel('Animals')
        plt.title('Herbivores in single cell')

    def color_map(self):
        colour = {'W': (0.0, 0.0, 1.0),
                  'L': (0.0, 0.6, 0.0),
                  'H': (0.5, 1.0, 0.5),
                  'D': (1.0, 1.0, 0.5)}

        colour_map = [[colour[column] for column in row]
                      for row in self.island_map.splitlines()]

        fig = plt.figure()
        image_axes = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # (start point, x), (start point y),
        image_axes.imshow(colour_map)

    def one_graph(self):
        self.make_graph()
        self.color_map()
        plt.show()
