from biosim import island_map
from biosim import landscapes
import pytest
import textwrap


class TestIslandMap:
    params_herb = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40.0,
        'phi_age': 0.6,
        'w_half': 10.0,
        'phi_weight': 0.1,
        'mu': 0.25,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10
    }

    params_carn = {
        'w_birth': 6.0,
        'sigma_birth': 1.0,
        'beta': 0.75,
        'eta': 0.125,
        'a_half': 40.0,
        'phi_age': 0.3,
        'w_half': 4.0,
        'phi_weight': 0.4,
        'mu': 0.4,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.8,
        'F': 50,
        'DeltaPhiMax': 10
    }

    @pytest.fixture(autouse=True)
    def create_map(self):
        islandmap = """\
        WWWWW
        WLLHW
        WLHHW
        WDDDW
        WWWWW"""
        islandmap = textwrap.dedent(islandmap)
        self.map = island_map.Map(islandmap)
        self.wat = landscapes.Water
        self.low = landscapes.Lowland
        self.high = landscapes.Highland
        self.des = landscapes.Dessert

    @pytest.fixture(autouse=True)
    def animals(self):
        self.animals_nr = 20
        self.animals_weight = 20
        self.animals_age = 5
        self.loc = (3, 3)
        self.herb_list = [{'loc': self.loc, 'pop':
                          [{'species': 'Herbivore', 'age': self.animals_age,
                           'weight': self.animals_weight}
                           for _ in range(self.animals_nr)]}]
        self.carn_list = [{'loc': self.loc, 'pop':
                          [{'species': 'Carnivore', 'age': self.animals_age,
                           'weight': self.animals_weight}
                           for _ in range(self.animals_nr)]}]

    def creates_map_and_adds_animals(self):
        self.map.creating_map()
        self.map.island_add_population(self.herb_list)
        self.map.island_add_population(self.carn_list)
        self.map.island_total_herbivores_and_carnivores()

    def test_validate_map_not_surounded_by_water(self):
        islandmap = """\
                WL
                WW"""
        islandmap = textwrap.dedent(islandmap)
        map = island_map.Map(islandmap)
        with pytest.raises(Exception):
            map.creating_map()

    def test_validate_map_not_right_letter(self):
        islandmap = """\
                WWW
                WKW
                WWW"""
        islandmap = textwrap.dedent(islandmap)
        map = island_map.Map(islandmap)
        with pytest.raises(Exception):
            map.creating_map()

    def test_validate_map_not_right_shape(self):
        islandmap = """\
                W
                WW"""
        islandmap = textwrap.dedent(islandmap)
        map = island_map.Map(islandmap)
        with pytest.raises(Exception):
            map.creating_map()

    def test_creating_map(self):
        self.map.creating_map()
        assert isinstance(self.map.map_dict, dict)

    def test_island_add_population(self):
        self.creates_map_and_adds_animals()
        self.map.island_total_herbivores_and_carnivores()
        self.map.island_total_sum_of_animals()
        assert self.map.island_total_carnivores == self.animals_nr
        assert self.map.island_total_herbivores == self.animals_nr
        assert self.map.island_total_animals == self.animals_nr * 2

    def test_island_migration(self, mocker):
        mocker.patch('random.random', return_value=0)
        self.creates_map_and_adds_animals()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.migrate()

        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                assert animal.has_migrated is True

        mocker.patch('random.random', return_value=1)
        self.creates_map_and_adds_animals()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.migrate()

        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                assert animal.has_migrated is False

    def test_migration_move_right(self, mocker):
        """
        If the random value is less than 0.25 the animal will move right
        :param mocker:
        :return:
        """
        mocker.patch('random.random', return_value=0.0)
        self.creates_map_and_adds_animals()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.has_migrated = True
            for animal in self.map.map_dict[loc].population_carn:
                animal.has_migrated = True

        for loc in self.map.map_dict.keys():
            self.map.island_migration_carn(loc)
            self.map.island_migration_herb(loc)
            self.map.map_dict[loc].cell_migration_remove()

        for loc in self.map.map_dict:
            self.map.map_dict[loc].cell_sum_of_animals()

        self.new_loc = (3, 4)  # This will be to the right for self.loc / (3,3)
        for loc in self.map.map_dict:
            if loc == self.new_loc:
                assert self.map.map_dict[loc].population_sum_herb == self.animals_nr
                assert self.map.map_dict[loc].population_sum_carn == self.animals_nr
            else:
                assert self.map.map_dict[loc].population_sum_herb == 0
                assert self.map.map_dict[loc].population_sum_carn == 0

    def test_migration_move_left(self, mocker):
        """
        If the random value is more than 0.25 and less than 0.5
         the animal will move left
        :param mocker:
        :return:
        """
        mocker.patch('random.random', return_value=0.35)  # This makes the animals move left
        self.creates_map_and_adds_animals()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.has_migrated = True
            for animal in self.map.map_dict[loc].population_carn:
                animal.has_migrated = True

        for loc in self.map.map_dict.keys():
            self.map.island_migration_carn(loc)
            self.map.island_migration_herb(loc)
            self.map.map_dict[loc].cell_migration_remove()

        for loc in self.map.map_dict:
            self.map.map_dict[loc].cell_sum_of_animals()

        self.new_loc = (3, 2)  # This will be to the left for self.loc / (3,3)
        for loc in self.map.map_dict:
            if loc == self.new_loc:
                assert self.map.map_dict[loc].population_sum_herb == self.animals_nr
                assert self.map.map_dict[loc].population_sum_carn == self.animals_nr
            else:
                assert self.map.map_dict[loc].population_sum_herb == 0
                assert self.map.map_dict[loc].population_sum_carn == 0

    def test_migration_move_up(self, mocker):
        """
        If the random value is more than 0.5 and less than 0.75
        the animals move up
        :param mocker:
        :return:
        """
        mocker.patch('random.random', return_value=0.65)  # This makes the animals move left
        self.creates_map_and_adds_animals()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.has_migrated = True
            for animal in self.map.map_dict[loc].population_carn:
                animal.has_migrated = True

        for loc in self.map.map_dict.keys():
            self.map.island_migration_carn(loc)
            self.map.island_migration_herb(loc)
            self.map.map_dict[loc].cell_migration_remove()

        for loc in self.map.map_dict:
            self.map.map_dict[loc].cell_sum_of_animals()

        self.new_loc = (2, 3)  # This will be up for self.loc / (3,3)
        for loc in self.map.map_dict:
            if loc == self.new_loc:
                assert self.map.map_dict[loc].population_sum_herb == self.animals_nr
                assert self.map.map_dict[loc].population_sum_carn == self.animals_nr
            else:
                assert self.map.map_dict[loc].population_sum_herb == 0
                assert self.map.map_dict[loc].population_sum_carn == 0

    def test_migration_move_down(self, mocker):
        """
        If the random value is more than 0.75
        the animals move down
        :param mocker:
        :return:
        """
        mocker.patch('random.random', return_value=0.9)  # This makes the animals move up
        self.creates_map_and_adds_animals()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.has_migrated = True
            for animal in self.map.map_dict[loc].population_carn:
                animal.has_migrated = True

        for loc in self.map.map_dict.keys():
            self.map.island_migration_carn(loc)
            self.map.island_migration_herb(loc)
            self.map.map_dict[loc].cell_migration_remove()

        for loc in self.map.map_dict:
            self.map.map_dict[loc].cell_sum_of_animals()

        self.new_loc = (4, 3)  # This will be down for self.loc / (3,3)
        for loc in self.map.map_dict:
            if loc == self.new_loc:
                assert self.map.map_dict[loc].population_sum_herb == self.animals_nr
                assert self.map.map_dict[loc].population_sum_carn == self.animals_nr
            else:
                assert self.map.map_dict[loc].population_sum_herb == 0
                assert self.map.map_dict[loc].population_sum_carn == 0

    def test_island_weight_loss(self):
        self.creates_map_and_adds_animals()
        self.map.island_weight_loss()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                assert animal.weight == self.animals_weight - (self.animals_weight * self.params_herb['eta'])

    def test_island_aging(self):
        self.creates_map_and_adds_animals()
        _nr_years = 4
        for _ in range(_nr_years):
            self.map.island_aging()
        self.map.island_total_sum_of_animals()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                assert animal.age == self.animals_age + _nr_years

    def test_island_feeding_herb(self):
        self.creates_map_and_adds_animals()
        self.map.island_feeding()
        self.map.island_total_sum_of_animals()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                assert animal.weight == self.animals_weight + self.params_herb['F'] * self.params_herb['beta']




    def test_island_feeding_carn(self):
        self.creates_map_and_adds_animals()
        self.map.island_feeding()
        self.map.island_total_sum_of_animals()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_carn:
                assert animal.weight

    def test_island_death(self):
        self.animals_weight = 0
        self.creates_map_and_adds_animals()
        self.map.island_total_sum_of_animals()
        assert self.map.island_total_animals == self.animals_nr * 2
        self.map.island_death()
        self.map.island_total_sum_of_animals()
        assert self.map.island_total_animals == 0

    def test_island_procreation(self, mocker):
        mocker.patch('random.random', return_value=0)
        self.creates_map_and_adds_animals()
        self.map.island_procreation()

        pass

    def test_one_year(self):
        self.map.island_feeding()
        self.map.island_procreation()
        self.map.island_migration()
        self.map.island_aging()
        self.map.island_weight_loss()
        self.map.island_death()
        self.map.island_total_herbivores_and_carnivores()
        self.map.island_total_sum_of_animals()

