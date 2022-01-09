from biosim import animals
import pytest

class TestAnimals:
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
    def create_herbivore(self):
        self.age_h = 5
        self.weight_h = 10
        self.herb = animals.Herbivore(self.age_h,self.weight_h)

    @pytest.fixture(autouse=True)
    def create_carnivore(self):
        self.age_c = 5
        self.weight_c = 20
        self.carn = animals.Carnivore(self.age_c,self.weight_c)


    def test_grow_one_year_test(self):
        """
        tests how good
        """

        age_herb = self.herb.age
        age_carn = self.carn.age

        for _ in range(10):
            self.herb.grow_one_year()
            self.carn.grow_one_year()
            assert self.herb.age == age_herb + 1
            assert self.carn.age == age_carn+ 1
            age_carn += 1
            age_herb += 1


    def test_weight_gained_from_eating_herbivore(self):

        for i in range(10):
            weight_real = self.herb.weight + self.params_herb['beta']*i
            self.herb.weight_gained_from_eating(i)
            assert self.herb.weight == weight_real


    def test_lost_weight(self):
        weight_herb = self.herb.weight
        weight_carn = self.carn.weight
        for i in range(10):
            weight_herb = weight_herb - self.params_herb['mu']*weight_herb
            weight_carn = weight_carn - self.params_carn['mu']*weight_carn
            self.herb.lose_weight()
            self.carn.lose_weight()
            assert self.herb.weight == weight_herb
            assert self.carn.weight == weight_carn

    def test_calculate_fitness(self):
        """
        tests the fitness calculation in the function
        """

        self.carn.weight = 0
        self.carn.calculate_fitness()
        assert self.carn.fitness == 0

        self.herb.calculate_fitness()
        assert self.herb.fitness == pytest.approx(0.4999999996)




