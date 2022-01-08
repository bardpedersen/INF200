"""
Different type of landscapes
Geogrofi
Migration
location
"""
import numpy as np
from biosim.landscapes import Lowland, Water, Highland, Dessert
import textwrap

class Map:
    def __init__(self, island_map):
        """
        Creates instance of map class

        :param: island_map: a multiline string representing the map
        """
        self.string_map = island_map  #Information we get from mono_ho
        self._landcape = {'W': Water(), 'L': Lowland(), 'H': Highland(), 'D': Dessert()}
        self.map = None

    @staticmethod
    def validate_map(string_map):
        """
        Checks if the borders of the map is water and all lines have the same lenght

        :param: string_map: a map in string format
        """

        for line in string_map.splitlines():
            assert len(string_map.splitlines()[0]) == len(line),'Map input not valid'
            assert line[0] == 'W','Map input not valid'
            assert line[len(line)-1] == 'W','Map input not valid'
            for ch in string_map.splitlines()[0]:
                assert ch == 'W','Map input not valid'
            for ch in string_map.splitlines()[len(string_map.splitlines())-1]:
                assert ch == 'W','Map input not valid'


    def creating_map(self):
        """
        makes string to dictionary with loc as key and landscape cell as value
        """
        self.validate_map(self.string_map)

        self.map = {}
        x = 1
        for line in self.string_map.splitlines():
            y = 1
            for ch in line:
                self.map[(x,y)] = self._landcape[ch]
                y+=1
            x+=1



    def island_add_population(self,ini_herb):
        """
        adds population to the map

        :param: ini_herb: is a dictionary containing both locatin and list of animals
        """

        for d in ini_herb:
            self.map[d['loc']].cell_add_population(d['pop'])

        self.map[d['loc']].cell_sum_of_animals()

    def island_feeding(self):
        """
        ages all the animals on the island
        """

        for key in self.map:
            if self.map[key].livable != False:
                self.map[key].cell_sum_of_animals()
                if self.map[key].population_sum_herb != None:
                    self.map[key].cell_add_fodder()
                    self.map[key].cell_feeding_herbivore()
                if self.map[key].population_sum_carn != None:
                    self.map[key].cell_feeding_carnivore()


    def island_procreation(self):
        """
        Birth of new animals in each cell
        """

        for key in self.map:
            if self.map[key].livable != False:
                self.map[key].cell_procreation()
                self.map[key].cell_sum_of_animals()



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
                self.map[key].cell_sum_of_animals()








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
                          for _ in range(20)]}]
    ini_carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(5)]}]
    island = Map(geogr)
    island.creating_map()
    island.island_add_population(ini_herbs)
    island.island_add_population(ini_carns)
    island.island_feeding()
    island.island_procreation()
    island.island_weight_loss()
    island.island_death()


    b = island.map

