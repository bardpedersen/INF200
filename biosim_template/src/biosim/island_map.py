"""
Different type of landscapes
Geogrofi
Migration
location
"""
from biosim.landscapes import Lowland, Water, Highland, Dessert
import textwrap
import random
import matplotlib.pyplot as plt
import numpy as np

random.seed(101)


class Map:
    def __init__(self, island_map):
        """
        Creates instance of map class

        :param island_map: a multiline string representing the map
        """
        self.string_map = island_map  #Information we get from mono_ho
        self.map_dict = None
        self.island_total_carnivores = None
        self.island_total_herbivores = None
        self.island_total_animals = None

    @staticmethod
    def validate_map(string_map):
        """
        Checks if the borders of the map is water and all lines have the same lenght

        :param string_map: a map in string format
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

        self.map_dict = {}
        x = 1
        for line in self.string_map.splitlines():
            y = 1
            for ch in line:
                cord = (x,y)
                landcape = {'W': Water(cord), 'L': Lowland(cord), 'H': Highland(cord), 'D': Dessert(cord)}
                assert landcape[ch] != KeyError, 'Letter dont match landtype'
                self.map_dict[cord] = landcape[ch]
                y+=1
            x+=1

    def island_add_population(self,ini_herb):
        """
        adds population to the map

        :param ini_herb: is a dictionary containing both locatin and list of animals
        """

        for d in ini_herb:
            self.map_dict[d['loc']].cell_add_population(d['pop'])

        self.map_dict[d['loc']].cell_sum_of_animals()

    def island_feeding(self):
        """
        feeds all the animals on the island
        """

        for key in self.map_dict:
            if self.map_dict[key].livable is True:
                self.map_dict[key].cell_sum_of_animals()
                if self.map_dict[key].population_sum_herb is not None:
                    self.map_dict[key].cell_add_fodder()
                    self.map_dict[key].cell_feeding_herbivore()
                if self.map_dict[key].population_sum_carn is not None:
                    self.map_dict[key].cell_feeding_carnivore()


    def island_procreation(self):
        """
        Birth of new animals in each cell
        """

        for key in self.map_dict:
            if self.map_dict[key].livable is True:
                self.map_dict[key].cell_procreation()
                self.map_dict[key].cell_sum_of_animals()

    def island_aging(self):
        """
        ages all the animals on the island
        """

        for key in self.map_dict:
            if self.map_dict[key].livable is True:
                self.map_dict[key].cell_aging()




    def island_migration(self):
        for loc in self.map_dict.keys():
            self.map_dict[loc].cell_migration()
            self.island_migration_carn(loc)
            self.island_migration_herb(loc)
            self.map_dict[loc].cell_migration_remove()

        for loc in self.map_dict:
            self.map_dict[loc].cell_sum_of_animals()

    def island_migration_herb(self, loc):
        for animal in self.map_dict[loc].population_herb:
            if animal.has_migrated:
                rand = random.random()
                if rand <= 0.25:
                    self.migration_move_right_herb(loc, animal)
                elif 0.25 < rand <= 0.5:
                    self.migration_move_left_herb(loc, animal)
                elif 0.5 < rand <= 0.75:
                    self.migration_move_up_herb(loc, animal)
                else:
                    self.migration_move_down_herb(loc, animal)

    def island_migration_carn(self, loc):
        for animal in self.map_dict[loc].population_carn:
            if animal.has_migrated:
                rand = random.random()
                if rand <= 0.25:
                    self.migration_move_right_carn(loc, animal)
                elif 0.25 < rand <= 0.5:
                    self.migration_move_left_carn(loc, animal)
                elif 0.5 < rand <= 0.75:
                    self.migration_move_up_carn(loc, animal)
                else:
                    self.migration_move_down_carn(loc, animal)

    def migration_move_right_herb(self, loc, animal):
        new_loc = (loc[0], loc[1] + 1)
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_herb.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_left_herb(self, loc, animal):
        new_loc = (loc[0], loc[1] - 1)
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_herb.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_up_herb(self, loc, animal):
        new_loc = (loc[0]-1, loc[1])
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_herb.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_down_herb(self, loc, animal):
        new_loc = (loc[0]+1, loc[1])
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_herb.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_right_carn(self, loc, animal):
        new_loc = (loc[0], loc[1] + 1)
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_carn.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_left_carn(self, loc, animal):
        new_loc = (loc[0], loc[1] - 1)
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_carn.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_up_carn(self, loc, animal):
        new_loc = (loc[0]-1, loc[1])
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_carn.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_down_carn(self, loc, animal):
        new_loc = (loc[0]+1, loc[1])
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_carn.append(animal)
        else:
            animal.has_migrated = False

    def island_weight_loss(self):
        """
        calculates the weight loss for each cell in simulation
        """
        for key in self.map_dict:
            if self.map_dict[key].livable is True:
                self.map_dict[key].cell_weight_lost()

    def island_death(self):
        """
        kills (by probability see animals.py) and removes the dead animal in each cells
        """
        for key in self.map_dict:
            if self.map_dict[key].livable is True:
                self.map_dict[key].cell_death()
                self.map_dict[key].cell_sum_of_animals()

    def island_total_herbivores_and_carnivores(self):
        """
        calculates the total of each species in the island
        """

        self.island_total_herbivores = 0
        self.island_total_carnivores = 0

        for key in self.map_dict:
            if self.map_dict[key].livable is True:
                self.map_dict[key].cell_sum_of_animals()
                self.island_total_herbivores += self.map_dict[key].population_sum_herb
                self.island_total_carnivores += self.map_dict[key].population_sum_carn

    def island_total_sum_of_animals(self):
        """
        calculates the total number of animals in each cell
        """

        self.island_total_animals = self.island_total_carnivores + self.island_total_herbivores


    def island_update_one_year(self):
        """
        updates the island one year
        """
        self.island_feeding()
        self.island_procreation()
        self.island_migration()
        self.island_aging()
        self.island_weight_loss()
        self.island_death()
        self.island_total_herbivores_and_carnivores()
        self.island_total_sum_of_animals()










if __name__ == '__main__':
    geogr = """\
               WWWW
               WLLW
               WLLW
               WWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (5, 5),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(1000)]}]
    ini_carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(20)]}]
    island = Map(geogr)
    island.creating_map()
    island.island_add_population(ini_herbs)
    for i in range(2):
        island.island_migration()
        island.island_aging()
        nested_list = list(map(list, island.string_map.splitlines()))
        x = 1
        for j in range(len(nested_list)):
            y = 1
            for k in range(len(nested_list[0])):
                if island.map_dict[(x, y)].population_sum_herb == None:
                    nested_list[j][k] = 0
                else:
                    nested_list[j][k] = island.map_dict[(x, y)].population_sum_herb
                y += 1
            x += 1
        matrix = np.array(nested_list)
        plt.imshow(matrix)
        plt.colorbar()
        plt.pause(1e-6)
        plt.show()
    island.island_total_herbivores_and_carnivores()
