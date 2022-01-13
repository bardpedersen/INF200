from biosim import island_map
from biosim import landscapes
import pytest
import textwrap

class TestIsland_Map():

    @pytest.fixture(autouse=True)
    def create_map(self):
        islandmap = """\
        WWWW
        WLHW
        WLDW
        WWWW"""
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
        self.loc = (2,2)
        self.herb_list = [{'loc': self.loc,'pop':
            [{'species': 'Herbivore','age': self.animals_age,
              'weight': self.animals_weight}
             for _ in range(self.animals_nr)]}]
        self.carn_list = [{'loc': self.loc,'pop':
            [{'species': 'Carnivore','age': self.animals_age,
              'weight': self.animals_weight}
             for _ in range(self.animals_nr)]}]

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

    def creates_map_and_adds_animals(self):
        self.map.creating_map()
        self.map.island_add_population(self.herb_list)
        self.map.island_add_population(self.carn_list)

    def test_island_add_population(self):
        self.creates_map_and_adds_animals()
        self.map.island_total_herbivores_and_carnivores()
        self.map.island_total_sum_of_animals()
        assert self.map.island_total_carnivores == self.animals_nr
        assert self.map.island_total_herbivores == self.animals_nr
        assert self.map.island_total_animals == self.animals_nr * 2

    """
    def test_island_feeding(self):
        self.creates_map_and_adds_animals()
        self.map.island_feeding()
        assert self.map.island_feeding()

        @patch('__main__.self.map.island_feeding()', return_value=1)
        def test_b(self):
            assert b == 0
    """

    def test_island_procreation(self):

        pass

    def test_island_aging(self):
        pass

    def test_island_migration(self):

        pass

    def test_migration_move_right(self):
        pass

    def test_migration_move_left(self):
        pass

    def test_migration_move_up(self):
        pass

    def test_migration_move_down(self):
        pass

    def test_island_weight_loss(self):
        pass

    def test_island_death(self):
        pass

    def test_island_total_herbivores_and_carnivores(self):
        pass

    def test_island_total_sum_of_animals(self):
        pass