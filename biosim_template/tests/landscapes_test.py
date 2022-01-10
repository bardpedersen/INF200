from biosim import landscapes
from biosim import animals
import pytest


class TestLandscapes:
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
    def create_landtype(self):
        self.lowland = landscapes.Lowland()
        self.highland = landscapes.Highland()
        self.dessert = landscapes.Dessert()
        self.water = landscapes.Water()

    @pytest.fixture(autouse=True)
    def animals(self):
        self.nr_animals = 20
        self.herb_list = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(self.nr_animals)]
        self.carn_list = [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(self.nr_animals)]

    def test_add_population_lowland(self):
        """
        Test that adding animals works.
        """

        self.lowland.cell_sum_of_animals()
        lowland_start_population_herb = self.lowland.population_sum_herb
        lowland_start_population_carn = self.lowland.population_sum_carn
        self.lowland.cell_add_population(self.herb_list)
        self.lowland.cell_add_population(self.carn_list)
        self.lowland.cell_sum_of_animals()
        lowland_end_population_herb = self.lowland.population_sum_herb
        lowland_end_population_carn = self.lowland.population_sum_carn

        assert lowland_start_population_herb == 0
        assert lowland_start_population_carn == 0
        assert lowland_end_population_herb == self.nr_animals
        assert lowland_end_population_carn == self.nr_animals

    def test_add_population_highland(self):

        self.highland.cell_sum_of_animals()
        highland_start_population_herb = self.highland.population_sum_herb
        highland_start_population_carn = self.highland.population_sum_carn
        self.highland.cell_add_population(self.herb_list)
        self.highland.cell_add_population(self.carn_list)
        self.highland.cell_sum_of_animals()
        highland_end_population_herb = self.highland.population_sum_herb
        highland_end_population_carn = self.highland.population_sum_carn

        assert highland_start_population_herb == 0
        assert highland_start_population_carn == 0
        assert highland_end_population_herb == self.nr_animals
        assert highland_end_population_carn == self.nr_animals

    def test_add_population_dessert(self):

        self.dessert.cell_sum_of_animals()
        dessert_start_population_herb = self.dessert.population_sum_herb
        dessert_start_population_carn = self.dessert.population_sum_carn
        self.dessert.cell_add_population(self.herb_list)
        self.dessert.cell_add_population(self.carn_list)
        self.dessert.cell_sum_of_animals()
        dessert_end_population_herb = self.dessert.population_sum_herb
        dessert_end_population_carn = self.dessert.population_sum_carn

        assert dessert_start_population_herb == 0
        assert dessert_start_population_carn == 0
        assert dessert_end_population_herb == self.nr_animals
        assert dessert_end_population_carn == self.nr_animals

    def test_add_population_water(self):

        self.water.cell_sum_of_animals()
        water_start_population_herb = self.water.population_sum_herb
        water_start_population_carn = self.water.population_sum_carn
        self.water.cell_add_population(self.herb_list)
        self.water.cell_add_population(self.carn_list)
        self.water.cell_sum_of_animals()
        water_end_population_herb = self.water.population_sum_herb
        water_end_population_carn = self.water.population_sum_carn

        assert water_start_population_herb == 0
        assert water_start_population_carn == 0
        assert water_end_population_herb == 0
        assert water_end_population_carn == 0

    def test_feeding_herb_lowland(self):
        self.lowland.cell_add_population(self.herb_list)
        self.lowland.cell_sum_of_animals()
        self.nr_animals = self.lowland.population_sum_herb

        lowland_fodder_before = self.lowland.fodder
        self.lowland.cell_add_fodder()
        lowland_fodder_before_eating = self.lowland.fodder
        self.lowland.cell_feeding_herbivore()
        lowland_fodder_after = self.lowland.fodder
        self.lowland.cell_add_fodder()
        lowland_fodder_regrows = self.lowland.fodder

        assert lowland_fodder_before == 0
        assert lowland_fodder_before_eating == self.lowland.params['f_max']
        assert lowland_fodder_after == self.lowland.params['f_max'] - (self.nr_animals * 10)
        assert lowland_fodder_regrows == self.lowland.params['f_max']

    def test_feeding_herb_highland(self):
        self.highland.cell_add_population(self.herb_list)
        self.highland.cell_sum_of_animals()
        self.nr_animals = self.highland.population_sum_herb

        highland_fodder_before = self.highland.fodder
        self.highland.cell_add_fodder()
        highland_fodder_before_eating = self.highland.fodder
        self.highland.cell_feeding_herbivore()
        highland_fodder_after = self.highland.fodder
        self.highland.cell_add_fodder()
        highland_fodder_regrows = self.highland.fodder

        assert highland_fodder_before == 0
        assert highland_fodder_before_eating == self.highland.params['f_max']
        assert highland_fodder_after == self.highland.params['f_max'] - (self.nr_animals * 10)
        assert highland_fodder_regrows == self.highland.params['f_max']

    def test_feeding_herb_dessert(self):
        self.dessert.cell_add_population(self.herb_list)
        self.dessert.cell_sum_of_animals()
        self.nr_animals = self.dessert.population_sum_herb

        dessert_fodder_before = self.dessert.fodder
        self.dessert.cell_add_fodder()
        dessert_fodder_before_eating = self.dessert.fodder
        self.dessert.cell_feeding_herbivore()
        dessert_fodder_after = self.dessert.fodder
        self.dessert.cell_add_fodder()
        dessert_fodder_regrows = self.dessert.fodder

        assert dessert_fodder_before == 0
        assert dessert_fodder_before_eating == self.dessert.params['f_max']
        assert dessert_fodder_after == self.dessert.params['f_max']
        assert dessert_fodder_regrows == self.dessert.params['f_max']

    def test_remove_population(self):  # Only lowland at the moment
        self.nr_animals = 100
        self.lowland.cell_add_population([{'species': 'Herbivore', 'age': 5, 'weight': 0}
                                          for _ in range(self.nr_animals)])
        self.lowland.cell_add_population([{'species': 'Carnivore', 'age': 5, 'weight': 0}
                                          for _ in range(self.nr_animals)])
        self.lowland.cell_sum_of_animals()
        lowland_start_population_herb = self.lowland.population_sum_herb
        lowland_start_population_carn = self.lowland.population_sum_carn

        self.lowland.cell_death()
        self.lowland.cell_sum_of_animals()

        lowland_end_population_herb = self.lowland.population_sum_herb
        lowland_end_population_carn = self.lowland.population_sum_carn

        assert lowland_start_population_herb == self.nr_animals
        assert lowland_start_population_carn == self.nr_animals
        assert lowland_end_population_herb < self.nr_animals
        assert lowland_end_population_carn < self.nr_animals

    def test_procreation(self):
        self.nr_animals = 20
        self.lowland.cell_add_population([{'species': 'Herbivore', 'age': 5, 'weight': 26}
                                          for _ in range(self.nr_animals)])
        self.lowland.cell_add_population([{'species': 'Carnivore', 'age': 5, 'weight': 26}
                                          for _ in range(self.nr_animals)])
        self.lowland.cell_sum_of_animals()
        lowland_start_population_herb = self.lowland.population_sum_herb
        lowland_start_population_carn = self.lowland.population_sum_carn

        self.lowland.cell_procreation()
        self.lowland.cell_sum_of_animals()

        lowland_end_population_herb = self.lowland.population_sum_herb
        lowland_end_population_carn = self.lowland.population_sum_carn

        assert lowland_start_population_herb == self.nr_animals
        assert lowland_start_population_carn == self.nr_animals
        assert lowland_end_population_herb == self.nr_animals  #No one is born
        assert lowland_end_population_carn == self.nr_animals  #is 1 of duplicating

    def test_migration(self):
        pass
