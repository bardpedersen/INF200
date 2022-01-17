"""
Different type of landscapes
Geography
Migration
location
"""
from biosim.landscapes import Lowland, Water, Highland, Dessert
import random
random.seed(101)


class Map:
    """class describing the map"""
    def __init__(self, island_map):
        """
        Creates instance of map class

        :param island_map: a multiline string representing the map
        """
        self.string_map = island_map  # Information we get from mono_ho
        self.map_dict = None
        self.island_total_carnivores = None
        self.island_total_herbivores = None
        self.island_total_animals = None

    @staticmethod
    def validate_map(string_map):
        """
        Checks if the borders of the map is water and all lines have the same length

        :param string_map: a map in string format
        """
        landscapes = ['W', 'L', 'H', 'D']

        for line in string_map.splitlines():
            if len(string_map.splitlines()[0]) != len(line):
                raise ValueError('Map lines must be of equal length')
            if line[0] != 'W':
                raise ValueError('Boundary must be Water')
            if line[len(line)-1] != 'W':
                raise ValueError('Boundary must be Water')
            for ch in line:
                if ch not in landscapes:
                    raise ValueError('Landscape type not valid')
        for ch in string_map.splitlines()[0]:
            if ch != 'W':
                raise ValueError('Boundary must be water')
        for ch in string_map.splitlines()[len(string_map.splitlines())-1]:
            if ch != 'W':
                raise ValueError('Boundary must be water')

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
                assert landcape[ch] != KeyError, 'Letter dont match land type'
                self.map_dict[cord] = landcape[ch]
                y += 1
            x += 1

    def island_add_population(self, ini_herb):
        """
        adds population to the map

        :param ini_herb: is a dictionary containing both location and list of animals
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
        """
        combines all the steps in the migration process
        """
        for loc in self.map_dict.keys():
            self.map_dict[loc].cell_migration()
            self.island_migration_carn(loc)
            self.island_migration_herb(loc)
            self.map_dict[loc].cell_migration_remove()

        for loc in self.map_dict:
            self.map_dict[loc].cell_sum_of_animals()

    def island_migration_herb(self, loc):
        """
        decides witch cell the herbivores migrates to

        :param loc: location of the animal before it moves
        """
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
        """
        decides witch cell the  migrates carnivore to

        :param loc: location of the animal before it moves
        """
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
        """
        moves a single herbivore right

        :param loc: current location of the animal
        :param animal: the animal to be moved
        """
        new_loc = (loc[0], loc[1] + 1)
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_herb.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_left_herb(self, loc, animal):
        """
        moves a single herbivore left

        :param loc: current location of the animal
        :param animal: the animal to be moved
        """
        new_loc = (loc[0], loc[1] - 1)
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_herb.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_up_herb(self, loc, animal):
        """
        moves a single animal up

        :param loc: current location of the animal
        :param animal: the herbivore to be moved
        """
        new_loc = (loc[0]-1, loc[1])
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_herb.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_down_herb(self, loc, animal):
        """
        moves a single hebivore down

        :param loc: current location of the animal
        :param animal: the animal to be moved
        """
        new_loc = (loc[0]+1, loc[1])
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_herb.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_right_carn(self, loc, animal):
        """
        moves a single carnivore right

        :param loc: current location of the animal
        :param animal: the animal to be moved
        """
        new_loc = (loc[0], loc[1] + 1)
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_carn.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_left_carn(self, loc, animal):
        """
        moves a single carnivore left

        :param loc: current location of the animal
        :param animal: the animal to be moved
        """
        new_loc = (loc[0], loc[1] - 1)
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_carn.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_up_carn(self, loc, animal):
        """
        moves a single carnivore up

        :param loc: current location of the animal
        :param animal: the animal to be moved
        """
        new_loc = (loc[0]-1, loc[1])
        if self.map_dict[new_loc].livable:
            self.map_dict[new_loc].population_carn.append(animal)
        else:
            animal.has_migrated = False

    def migration_move_down_carn(self, loc, animal):
        """
        moves a single carnivore down

        :param loc: current location of the animal
        :param animal: the animal to be moved
        """
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
        self.island_total_herbivores_and_carnivores()

        herb = self.island_total_herbivores
        if herb is None:
            herb = 0
        carn = self.island_total_carnivores
        if carn is None:
            carn = 0

        pop = carn + herb
        if pop == 0:
            pop = None
        self.island_total_animals = pop

    def island_age_weight_fitness(self):
        """
        adds the all of the ages weights of the animals into a dict
        """

        herb_island = {
            'age': [],
            'weight': [],
            'fitness': []
        }
        carn_island = {
            'age': [],
            'weight': [],
            'fitness': []
        }
        for cord in self.map_dict.keys():
            herb, carn = self.map_dict[cord].cell_age_weight_and_fitness()
            for key in herb:
                herb_island[key].extend(herb[key])
            for key in carn:
                carn_island[key].extend(carn[key])
        return herb_island, carn_island

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
