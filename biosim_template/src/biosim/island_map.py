"""
Different type of landscapes
Geogrofi
Migration
location
"""
from biosim.landscapes import Lowland, Water, Highland, Dessert
import textwrap
import random


class Map:
    def __init__(self, island_map):
        """
        Creates instance of map class

        :param: island_map: a multiline string representing the map
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

        self.map_dict = {}
        x = 1
        for line in self.string_map.splitlines():
            y = 1
            for ch in line:
                cord = (x, y)
                landcape = {'W': Water(cord), 'L': Lowland(cord), 'H': Highland(cord), 'D': Dessert(cord)}
                self.map_dict[(x, y)] = landcape[ch]
                y+=1
            x+=1

    def island_add_population(self,ini_herb):
        """
        adds population to the map

        :param: ini_herb: is a dictionary containing both location and list of animals
        """

        for d in ini_herb:
            self.map_dict[d['loc']].cell_add_population(d['pop'])

        #self.map_dict[d['loc']].cell_sum_of_animals()

    def island_feeding(self):
        """
        ages all the animals on the island
        """

        for key in self.map_dict:
            if self.map_dict[key]._livable is True:
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
            if self.map_dict[key]._livable is True:
                self.map_dict[key].cell_procreation()
                self.map_dict[key].cell_sum_of_animals()



    def island_aging(self):
        """
        ages all the animals on the island
        """

        for key in self.map_dict:
            if self.map_dict[key]._livable is True:
                self.map_dict[key].cell_aging()

    def island_migration_list(self):
        for loc in self.map_dict:
            self.map_dict[loc].cell_migration()

    def island_migration(self):
        self.island_migration_list()
        for loc in self.map_dict:
            for animal in self.map_dict[loc].are_migrating:
                rand = random.random()
                if rand <= 0.25:
                    self.migration_move_right(loc, animal)
                elif 0.25 < rand <= 0.5:
                    self.migration_move_left(loc, animal)
                elif 0.5 < rand <= 0.75:
                    self.migration_move_up(loc, animal)
                else:
                    self.migration_move_down(loc, animal)
            self.map_dict[loc].are_migrating = []

        for loc in self.map_dict:
            self.map_dict[loc].cell_sum_of_animals()

    def migration_move_right(self, loc, animal):
        new_loc = (loc[0], loc[1] + 1)
        if self.map_dict[new_loc].livable:
            if type(animal).__name__ == 'Herbivore':
                self.map_dict[new_loc].population_herb.append(animal)
            elif type(animal).__name__ == 'Carnivore':
                self.map_dict[new_loc].population_carn.append(animal)
        else:
            if type(animal).__name__ == 'Herbivore':
                self.map_dict[loc].population_herb.append(animal)
            elif type(animal).__name__ == 'Carnivore':
                self.map_dict[loc].population_carn.append(animal)

    def migration_move_left(self, loc, animal):
        new_loc = (loc[0], loc[1] - 1)
        if self.map_dict[new_loc].livable:
            if type(animal).__name__ == 'Herbivore':
                self.map_dict[new_loc].population_herb.append(animal)
            elif type(animal).__name__ == 'Carnivore':
                self.map_dict[new_loc].population_carn.append(animal)
        else:
            if type(animal).__name__ == 'Herbivore':
                self.map_dict[loc].population_herb.append(animal)
            elif type(animal).__name__ == 'Carnivore':
                self.map_dict[loc].population_carn.append(animal)

    def migration_move_up(self, loc, animal):
        new_loc = (loc[0]-1, loc[1])
        if self.map_dict[new_loc].livable:
            if type(animal).__name__ == 'Herbivore':
                self.map_dict[new_loc].population_herb.append(animal)
            elif type(animal).__name__ == 'Carnivore':
                self.map_dict[new_loc].population_carn.append(animal)
        else:
            if type(animal).__name__ == 'Herbivore':
                self.map_dict[loc].population_herb.append(animal)
            elif type(animal).__name__ == 'Carnivore':
                self.map_dict[loc].population_carn.append(animal)

    def migration_move_down(self, loc, animal):
        new_loc = (loc[0]+1, loc[1])
        if self.map_dict[new_loc].livable:
            if type(animal).__name__ == 'Herbivore':
                self.map_dict[new_loc].population_herb.append(animal)
            elif type(animal).__name__ == 'Carnivore':
                self.map_dict[new_loc].population_carn.append(animal)
        else:
            if type(animal).__name__ == 'Herbivore':
                self.map_dict[loc].population_herb.append(animal)
            elif type(animal).__name__ == 'Carnivore':
                self.map_dict[loc].population_carn.append(animal)


    def island_weight_loss(self):
        """
        calculates the weight loss for each cell in simulation
        """
        for key in self.map_dict:
            if self.map_dict[key]._livable is True:
                self.map_dict[key].cell_weight_lost()

    def island_death(self):
        """
        kills (by probability see animals.py) and removes the dead animal in each cells
        """
        for key in self.map_dict:
            if self.map_dict[key]._livable is True:
                self.map_dict[key].cell_death()
                self.map_dict[key].cell_sum_of_animals()

    def island_total_herbivores_and_carnivores(self):
        """
        calculates the total of each species in the island
        """

        self.island_total_herbivores = 0
        self.island_total_carnivores = 0

        for key in self.map_dict:
            if self.map_dict[key]._livable is True:
                self.map_dict[key].cell_sum_of_animals()
                self.island_total_herbivores += self.map_dict[key].population_sum_herb
                self.island_total_carnivores += self.map_dict[key].population_sum_carn

    def island_total_sum_of_animals(self):
        """
        calculates the total number of animals in each cell
        """

        self.island_total_animals = self.island_total_carnivores + self.island_total_herbivores













if __name__ == '__main__':
    geogr = """\
               WWW
               WLW
               WLW
               WWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]
    ini_carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(20)]}]
    island = Map(geogr)
    island.creating_map()
    island.island_add_population(ini_herbs)

    for i in range(50):


        island.island_feeding()
        island.island_procreation()
        island.island_aging()
        island.island_weight_loss()
        island.island_death()

    island.island_add_population(ini_carns)
    for i in range(50):
        island.island_feeding()
        island.island_procreation()
        island.island_aging()
        island.island_weight_loss()
        island.island_death()

    b = island.map_dict
