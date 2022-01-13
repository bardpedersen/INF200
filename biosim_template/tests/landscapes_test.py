from biosim.simulation import Lowland, Highland, Dessert, Water
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
        self.lowland = Lowland((1, 1))
        self.highland = Highland((1, 2))
        self.dessert = Dessert((2, 1))
        self.water = Water((2, 2))

    @pytest.fixture(autouse=True)
    def animals(self):
        self.animals_nr = 20
        self.animals_weight = 20
        self.animals_age = 5
        self.herb_list = [{'species': 'Herbivore', 'age': self.animals_age, 'weight': self.animals_weight}
                          for _ in range(self.animals_nr)]
        self.carn_list = [{'species': 'Carnivore', 'age': self.animals_age, 'weight': self.animals_weight}
                          for _ in range(self.animals_nr)]

    """"
    @pytest.mark.parametrize('class_to_test',[Lowland, Highland, Dessert, Water])
    def test_add_animals(class_to_test):
        animals_nr = 20
        animals_weight = 20
        animals_age = 5
        herb_list = [{'species': 'Herbivore', 'age': animals_age, 'weight': animals_weight}
                     for _ in range(animals_nr)]
        carn_list = [{'species': 'Carnivore', 'age': animals_age, 'weight': animals_weight}
                     for _ in range(animals_nr)]

        obj = class_to_test()
        start_population_herb = obj.population_sum_herb
        start_population_carn = obj.population_sum_carn
        obj.cell_add_population(herb_list)
        obj.cell_add_population(carn_list)
        end_population_herb = obj.population_sum_herb
        end_population_carn = obj.population_sum_carn

        assert start_population_herb == animals_nr
        assert start_population_carn == animals_nr
        assert end_population_herb == animals_nr + animals_nr
        assert end_population_carn == animals_nr + animals_nr
    """

    def add_animals_lowland(self):
        self.lowland.cell_add_population(self.herb_list)
        self.lowland.cell_add_population(self.carn_list)
        self.lowland.cell_sum_of_animals()

    def add_animals_highland(self):
        self.highland.cell_add_population(self.herb_list)
        self.highland.cell_add_population(self.carn_list)
        self.highland.cell_sum_of_animals()

    def add_animals_dessert(self):
        self.dessert.cell_add_population(self.herb_list)
        self.dessert.cell_add_population(self.carn_list)
        self.dessert.cell_sum_of_animals()

    def add_animals_water(self):
        self.water.cell_add_population(self.herb_list)
        self.water.cell_add_population(self.carn_list)
        self.water.cell_sum_of_animals()

    def test_add_population_lowland(self):
        """
        Test that adding animals works in lowland.
        """
        self.add_animals_lowland()
        lowland_start_population_herb = self.lowland.population_sum_herb
        lowland_start_population_carn = self.lowland.population_sum_carn
        self.lowland.cell_add_population(self.herb_list)
        self.lowland.cell_add_population(self.carn_list)
        self.lowland.cell_sum_of_animals()
        lowland_end_population_herb = self.lowland.population_sum_herb
        lowland_end_population_carn = self.lowland.population_sum_carn

        assert lowland_start_population_herb == self.animals_nr
        assert lowland_start_population_carn == self.animals_nr
        assert lowland_end_population_herb == self.animals_nr + self.animals_nr
        assert lowland_end_population_carn == self.animals_nr + self.animals_nr

    def test_add_population_highland(self):
        """
        Test that adding animals works in highland.
        """
        self.add_animals_highland()
        highland_start_population_herb = self.highland.population_sum_herb
        highland_start_population_carn = self.highland.population_sum_carn
        self.highland.cell_add_population(self.herb_list)
        self.highland.cell_add_population(self.carn_list)
        self.highland.cell_sum_of_animals()
        highland_end_population_herb = self.highland.population_sum_herb
        highland_end_population_carn = self.highland.population_sum_carn

        assert highland_start_population_herb == self.animals_nr
        assert highland_start_population_carn == self.animals_nr
        assert highland_end_population_herb == self.animals_nr + self.animals_nr
        assert highland_end_population_carn == self.animals_nr + self.animals_nr

    def test_add_population_dessert(self):
        """
        Test that adding animals works in dessert.
        """
        self.add_animals_dessert()
        dessert_start_population_herb = self.dessert.population_sum_herb
        dessert_start_population_carn = self.dessert.population_sum_carn
        self.dessert.cell_add_population(self.herb_list)
        self.dessert.cell_add_population(self.carn_list)
        self.dessert.cell_sum_of_animals()
        dessert_end_population_herb = self.dessert.population_sum_herb
        dessert_end_population_carn = self.dessert.population_sum_carn

        assert dessert_start_population_herb == self.animals_nr
        assert dessert_start_population_carn == self.animals_nr
        assert dessert_end_population_herb == self.animals_nr + self.animals_nr
        assert dessert_end_population_carn == self.animals_nr + self.animals_nr

    def test_add_population_water(self):
        """
        Test that adding animals don't works in water.
        """
        self.add_animals_water()
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

    def test_regrowth_lowland(self):
        """
        Test that regrowth works
        """
        self.add_animals_lowland()

        lowland_fodder_before = self.lowland.fodder
        self.lowland.cell_add_fodder()
        lowland_fodder_before_eating = self.lowland.fodder
        self.lowland.cell_feeding_herbivore()
        lowland_fodder_after_eating = self.lowland.fodder
        self.lowland.cell_add_fodder()
        lowland_fodder_regrows = self.lowland.fodder

        assert lowland_fodder_before == 0
        assert lowland_fodder_before_eating == self.lowland.params['f_max']
        assert lowland_fodder_after_eating == self.lowland.params['f_max'] - (self.animals_nr * self.params_herb['F'])
        assert lowland_fodder_regrows == self.lowland.params['f_max']

    def test_regrowth_highland(self):
        """
        Test that regrowth works
        """
        self.add_animals_highland()

        highland_fodder_before = self.highland.fodder
        self.highland.cell_add_fodder()
        highland_fodder_before_eating = self.highland.fodder
        self.highland.cell_feeding_herbivore()
        highland_fodder_after = self.highland.fodder
        self.highland.cell_add_fodder()
        highland_fodder_regrows = self.highland.fodder

        assert highland_fodder_before == 0
        assert highland_fodder_before_eating == self.highland.params['f_max']
        assert highland_fodder_after == self.highland.params['f_max'] - (self.animals_nr * self.params_herb['F'])
        assert highland_fodder_regrows == self.highland.params['f_max']

    def test_regrowth_dessert(self):
        """
        Test that regrowth works
        """
        self.add_animals_dessert()

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

    def test_regrowth_water(self):
        """
        Test that regrowth works
        """
        self.add_animals_water()

        water_fodder_before = self.water.fodder
        self.water.cell_add_fodder()
        water_fodder_before_eating = self.water.fodder
        self.water.cell_feeding_herbivore()
        water_fodder_after = self.water.fodder
        self.water.cell_add_fodder()
        water_fodder_regrows = self.water.fodder

        assert water_fodder_before == 0
        assert water_fodder_before_eating == self.water.params['f_max']
        assert water_fodder_after == self.water.params['f_max']
        assert water_fodder_regrows == self.water.params['f_max']

    def test_feeding_herb_lowland(self):
        self.add_animals_lowland()
        total_weight_before = 0
        total_weight_after = 0
        for animal in self.lowland.population_herb:
            total_weight_before += animal.weight
        average_weight_before_eat = total_weight_before / self.animals_nr
        self.lowland.cell_add_fodder()
        self.lowland.cell_feeding_herbivore()
        for animal in self.lowland.population_herb:
            total_weight_after += animal.weight
        average_weight_after_eat = total_weight_after / self.animals_nr

        assert average_weight_before_eat == self.animals_weight
        assert average_weight_after_eat == self.animals_weight + self.params_herb['F'] * self.params_herb['beta']

    def test_feeding_herb_highland(self):
        self.add_animals_highland()
        total_weight_before = 0
        total_weight_after = 0
        for animal in self.highland.population_herb:
            total_weight_before += animal.weight
        average_weight_before_eat = total_weight_before / self.animals_nr
        self.highland.cell_add_fodder()
        self.highland.cell_feeding_herbivore()
        for animal in self.highland.population_herb:
            total_weight_after += animal.weight
        average_weight_after_eat = total_weight_after / self.animals_nr

        assert average_weight_before_eat == self.animals_weight
        assert average_weight_after_eat == self.animals_weight + self.params_herb['F'] * self.params_herb['beta']

    def test_feeding_herb_dessert(self):
        self.add_animals_dessert()
        total_weight_before = 0
        total_weight_after = 0
        for animal in self.dessert.population_herb:
            total_weight_before += animal.weight
        average_weight_before_eat = total_weight_before / self.animals_nr
        self.dessert.cell_add_fodder()
        self.dessert.cell_feeding_herbivore()
        for animal in self.dessert.population_herb:
            total_weight_after += animal.weight
        average_weight_after_eat = total_weight_after / self.animals_nr

        assert average_weight_before_eat == self.animals_weight
        assert average_weight_after_eat == self.animals_weight

    def test_feeding_herb_water(self):
        self.add_animals_water()
        total_weight_before = 0
        total_weight_after = 0
        for animal in self.water.population_herb:
            total_weight_before += animal.weight
        average_weight_before_eat = total_weight_before / self.animals_nr
        self.water.cell_add_fodder()
        self.water.cell_feeding_herbivore()
        for animal in self.water.population_herb:
            total_weight_after += animal.weight
        average_weight_after_eat = total_weight_after / self.animals_nr

        assert average_weight_before_eat == 0
        assert average_weight_after_eat == 0

    def test_aging_lowland(self):
        """
        Test that animals age, once per called upon
        """
        self.add_animals_lowland()

        total_age_before_herb = 0
        total_age_before_carn = 0
        for animal in self.lowland.population_herb:
            total_age_before_herb += animal.age
        average_age_before_herb = total_age_before_herb / self.animals_nr

        for animal in self.lowland.population_carn:
            total_age_before_carn += animal.age
        average_age_before_carn = total_age_before_carn / self.animals_nr

        _nr_years = 2
        for _ in range(_nr_years):
            self.lowland.cell_aging()

        total_age_after_herb = 0
        total_age_after_carn = 0
        for animal in self.lowland.population_herb:
            total_age_after_herb += animal.age
        average_age_after_herb = total_age_after_herb / self.animals_nr

        for animal in self.lowland.population_carn:
            total_age_after_carn += animal.age
        average_age_after_carn = total_age_after_carn / self.animals_nr

        assert average_age_before_herb == self.animals_age
        assert average_age_before_carn == self.animals_age
        assert average_age_after_herb == self.animals_age + _nr_years
        assert average_age_after_carn == self.animals_age + _nr_years

    def test_aging_highland(self):
        """
        Test that animals age, once per called upon
        """
        self.add_animals_highland()

        total_age_before_herb = 0
        total_age_before_carn = 0
        for animal in self.highland.population_herb:
            total_age_before_herb += animal.age
        average_age_before_herb = total_age_before_herb / self.animals_nr

        for animal in self.highland.population_carn:
            total_age_before_carn += animal.age
        average_age_before_carn = total_age_before_carn / self.animals_nr

        _nr_years = 2
        for _ in range(_nr_years):
            self.highland.cell_aging()

        total_age_after_herb = 0
        total_age_after_carn = 0
        for animal in self.highland.population_herb:
            total_age_after_herb += animal.age
        average_age_after_herb = total_age_after_herb / self.animals_nr

        for animal in self.highland.population_carn:
            total_age_after_carn += animal.age
        average_age_after_carn = total_age_after_carn / self.animals_nr

        assert average_age_before_herb == self.animals_age
        assert average_age_before_carn == self.animals_age
        assert average_age_after_herb == self.animals_age + _nr_years
        assert average_age_after_carn == self.animals_age + _nr_years

    def test_aging_dessert(self):
        """
        Test that animals age, once per called upon
        """
        self.add_animals_dessert()

        total_age_before_herb = 0
        total_age_before_carn = 0
        for animal in self.dessert.population_herb:
            total_age_before_herb += animal.age
        average_age_before_herb = total_age_before_herb / self.animals_nr

        for animal in self.dessert.population_carn:
            total_age_before_carn += animal.age
        average_age_before_carn = total_age_before_carn / self.animals_nr

        _nr_years = 2
        for _ in range(_nr_years):
            self.dessert.cell_aging()

        total_age_after_herb = 0
        total_age_after_carn = 0
        for animal in self.dessert.population_herb:
            total_age_after_herb += animal.age
        average_age_after_herb = total_age_after_herb / self.animals_nr

        for animal in self.dessert.population_carn:
            total_age_after_carn += animal.age
        average_age_after_carn = total_age_after_carn / self.animals_nr

        assert average_age_before_herb == self.animals_age
        assert average_age_before_carn == self.animals_age
        assert average_age_after_herb == self.animals_age + _nr_years
        assert average_age_after_carn == self.animals_age + _nr_years

    def test_aging_water(self):
        """
        Test that animals age, once per called upon
        """
        self.add_animals_water()

        total_age_before_herb = 0
        total_age_before_carn = 0
        for animal in self.water.population_herb:
            total_age_before_herb += animal.age
        average_age_before_herb = total_age_before_herb / self.animals_nr

        for animal in self.water.population_carn:
            total_age_before_carn += animal.age
        average_age_before_carn = total_age_before_carn / self.animals_nr

        _nr_years = 2
        for _ in range(_nr_years):
            self.water.cell_aging()

        total_age_after_herb = 0
        total_age_after_carn = 0
        for animal in self.water.population_herb:
            total_age_after_herb += animal.age
        average_age_after_herb = total_age_after_herb / self.animals_nr

        for animal in self.water.population_carn:
            total_age_after_carn += animal.age
        average_age_after_carn = total_age_after_carn / self.animals_nr

        assert average_age_before_herb == 0
        assert average_age_before_carn == 0
        assert average_age_after_herb == 0
        assert average_age_after_carn == 0






    def test_death_lowland(self):
        """
        Test that animals die, animals die with certain when weight = 0
        """
        self.lowland.cell_add_population([{'species': 'Herbivore', 'age': 5, 'weight': 0}
                                          for _ in range(self.animals_nr)])
        self.lowland.cell_add_population([{'species': 'Carnivore', 'age': 5, 'weight': 0}
                                          for _ in range(self.animals_nr)])
        self.lowland.cell_sum_of_animals()
        lowland_start_population_herb = self.lowland.population_sum_herb
        lowland_start_population_carn = self.lowland.population_sum_carn

        self.lowland.cell_death()
        self.lowland.cell_sum_of_animals()

        lowland_end_population_herb = self.lowland.population_sum_herb
        lowland_end_population_carn = self.lowland.population_sum_carn

        assert lowland_start_population_herb == self.animals_nr
        assert lowland_start_population_carn == self.animals_nr
        assert lowland_end_population_herb == 0
        assert lowland_end_population_carn == 0

    def test_procreation(self):
        """
        Test that if there are more than one animal, the number of animals will increase.
        :return:
        """
        self.add_animals_lowland()

        lowland_start_population_herb = self.lowland.population_sum_herb
        lowland_start_population_carn = self.lowland.population_sum_carn

        self.lowland.cell_procreation()
        self.lowland.cell_procreation()

        self.lowland.cell_sum_of_animals()

        lowland_end_population_herb = self.lowland.population_sum_herb
        lowland_end_population_carn = self.lowland.population_sum_carn

        assert lowland_start_population_herb == self.animals_nr
        assert lowland_start_population_carn == self.animals_nr
        assert lowland_end_population_herb == self.animals_nr  # No one is born
        assert lowland_end_population_carn == self.animals_nr  # is 1 of duplicating

    def test_feeding_carnivores(self):
        """
        Test that carnivores feed
        Both that herbivores are removed as well as
        carnivores gain weight
        :return:
        """
        self.add_animals_lowland()

        lowland_start_herbivores = self.lowland.population_sum_herb
        total_weight_before_eat = 0
        for animal in self.lowland.population_carn:
            total_weight_before_eat += animal.weight
        average_weight_before_eat = total_weight_before_eat / self.animals_nr

        self.lowland.cell_feeding_carnivore()
        self.lowland.cell_sum_of_animals()

        lowland_end_herbivores = self.lowland.population_sum_herb
        total_weight_after_eat = 0
        for animal in self.lowland.population_carn:
            total_weight_after_eat += animal.weight
        average_weight_after_eat = total_weight_after_eat / self.animals_nr

        assert lowland_start_herbivores == self.animals_nr
        assert lowland_end_herbivores < self.animals_nr
        assert average_weight_before_eat == self.animals_weight
        assert average_weight_after_eat > self.animals_weight

    def test_feed_with_fitness_order(self):
        """
        Test that they feed by fitness order
        :return:
        """
        self.add_animals_lowland()

        self.lowland.cell_calculate_fitness()
        lowland_start_fitness_herb = self.lowland.population_herb[4].fitness
        self.lowland.population_herb.sort(key=lambda x: x.fitness, reverse=True)
        self.lowland.population_carn.sort(key=lambda x: x.fitness, reverse=True)
        pass

    def test_migration_lowland_to_lowland_prob_max(self, mocker):
        """
        Test that the migration works
        :return:
        """
        mocker.patch('random.random', return_value=0)
        self.add_animals_lowland()
        self.lowland.cell_migration()
        animals_migrating = 0
        animals_not_migrating = 0
        for animal in self.lowland.population_herb:
            if animal.has_migrated == True:
                animals_migrating += 1
            else:
                animals_not_migrating += 1

        self.lowland.cell_sum_of_animals()
        self.highland.cell_sum_of_animals()
        self.dessert.cell_sum_of_animals()
        self.water.cell_sum_of_animals()

        self.lowland.cell_migration_remove()
        self.lowland.cell_sum_of_animals()

        assert animals_migrating == self.animals_nr
        assert animals_not_migrating == self.animals_nr - animals_migrating

        assert self.lowland.population_sum_herb == 0
        assert self.highland.population_sum_herb == 0
        assert self.dessert.population_sum_herb == 0
        assert self.water.population_sum_herb == 0

    def test_migration_lowland_to_lowland_prob_zero(self, mocker):
        """
        Test that the migration works
        :return:
        from the task, and the fitnes forula, wi kan calculate that the fitness * mu = 0.182765.
        So any random value lower, vil make all animals migrate, anything over vil stop all animals from migrating.
        """
        mocker.patch('random.random', return_value=1)
        self.add_animals_lowland()
        self.lowland.cell_migration()
        animals_migrating = 0
        animals_not_migrating = 0
        for animal in self.lowland.population_herb:
            if animal.has_migrated == True:
                animals_migrating += 1
            else:
                animals_not_migrating += 1

        self.lowland.cell_sum_of_animals()
        self.highland.cell_sum_of_animals()
        self.dessert.cell_sum_of_animals()
        self.water.cell_sum_of_animals()

        assert animals_migrating == 0
        assert animals_not_migrating == self.animals_nr - animals_migrating

        assert self.lowland.population_sum_herb == self.animals_nr
        assert self.highland.population_sum_herb == 0
        assert self.dessert.population_sum_herb == 0
        assert self.water.population_sum_herb == 0
        assert self.lowland.population_sum_herb + self.highland.population_sum_herb +\
               self.dessert.population_sum_herb + self.water.population_sum_herb == self.animals_nr
