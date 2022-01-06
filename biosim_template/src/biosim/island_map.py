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
        """
        Creates instance of map class

        :param: island_map: a multiline string representing the map
        """
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


    def island_add_population(self,ini_herb):
        """
        adds population to the map

        :param: ini_herb: is a dictionary containing both locatin and list of animals
        """

        for d in ini_herb:
            self.map[d['loc']].cell_add_population(d['pop'])

        self.map[d['loc']].cell_sum_of_herbivores()

    def island_feeding(self):
        """
        ages all the animals on the island
        """

        for key in self.map:
            if self.map[key].livable != False:

                self.map[key].cell_add_fodder()
                self.map[key].cell_feeding()


    def island_procreation(self):
        """
        Birth of new animals in each cell
        """

        for key in self.map:
            if self.map[key].livable != False:
                self.map[key].cell_procreation()
                self.map[key].cell_sum_of_herbivores()



    def island_aging(self):
        """
        ages all the animals on the island
        """

        for key in self.map:
            if self.map[key].livable != False:
                self.map[key].cell_aging()


    def island_migration(self):
        pass


    def island_weight_loss(self):
        for key in self.map:
            if self.map[key].livable != False:
                self.map[key].cell_weight_lost()

    def island_death(self):
        for key in self.map:
            if self.map[key].livable != False:
                self.map[key].cell_death()
                self.map[key].cell_sum_of_herbivores()






        pass
if __name__=='__main__':
    geogr = """\
               WWW
               WLW
               WWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]
    island = Map(geogr)
    island.creating_map()
    island.island_add_population(ini_herbs)
    island.island_feeding()
    island.island_procreation()
    island.island_weight_loss()
    island.island_death()


    b = island.map

