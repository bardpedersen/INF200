from biosim.animals import Herbivore
from biosim.landscapes import LowLand, Water
from biosim.island_map import Map

import numpy as np
import matplotlib.pyplot as plt


class WindowPlot:
    def __init__(self, island_map):
        self.x_list = []
        self.y_list = []
        self.island_map = island_map

    def update_graph_x(self, year):
        self.x_list.append(year)

    def update_graph_y(self, num_animals):
        self.y_list.append(num_animals)

    def make_graph(self):
        plt.plot(self.x_list, self.y_list)
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
        image_axes = fig.add_axes([0.1, 0.1, 0.7, 0.8])#(start point, x), (start point y),
        image_axes.imshow(colour_map)

    def one_graph(self):
        self.make_graph()
        self.color_map()
        plt.show()
