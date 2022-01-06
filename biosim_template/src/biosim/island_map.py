"""
Different type of landscapes
Geogrofi
Migration
location
"""
import numpy as np
from biosim.landscapes import LowLand, Water
from biosim.animals import Herbivore

class Map:
    def __init__(self, island_map):
        self._map = island_map  #Information we get from mono_ho
        self._landcape = {'W': Water,
                          'L': LowLand}

        self.cells = self.creating_island #Individual cells that make up the map.

    def creating_island(self):
        """
        first str to matirx
        """
        map_str_clean = self._map.replace(' ', '')  #Removes empty lines
        matrix_map = np.array([[j for j in i] for i in map_str_clean.splitlines()]) #Splits the str to array/matrix
        """
        Turn each symbols to right landscape
        """
        cells_with_land = np.empty(self.matrix_map.shape, dtype=object)
        for i, k in enumerate(matrix_map):
            for j, _letter in enumerate(k): #i and j is the cordinates, letter is the landscape of the cordinates
                cells_with_land[i][j] = self._landcape[_letter]

        return cells_with_land


    def migration(self):
        """No migration on one cell island"""
        pass


