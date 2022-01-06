"""
Different type of landscapes
Geogrofi
Migration
location
"""
import numpy as np
from biosim.landscapes import LowLand, Water
from biosim.animals import Herbivore
import textwrap

class Map:
    def __init__(self, island_map):
        self.island_map = island_map  #Information we get from mono_ho
        self._landcape = {'W': Water(),'L': LowLand()}
        self.map = None

    def creating_map(self):
        """
        makes string to dictionary with loc as key and landscape cell as value
        """
        self.map = {}
        matrix_map = list(map(list,self.island_map.splitlines()))
        for i in range(len(matrix_map)):
            for j in range(len(matrix_map[0])):
                self.map[(i+1),(j+1)] = self._landcape[matrix_map[i][j]]


    def add_population(self,ini_herb):
        """
        adds population to the map

        :param: ini_herb: is a dictionary containing both locatin and list of animals
        """

