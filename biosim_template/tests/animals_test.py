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
        self.herb = animals.Herbivore(self.age_h, self.weight_h)

    @pytest.fixture(autouse=True)
    def create_carnivore(self):
        self.age_c = 5
        self.weight_c = 20
        self.carn = animals.Carnivore(self.age_c, self.weight_c)
        yield

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
            assert self.carn.age == age_carn + 1
            age_carn += 1
            age_herb += 1

    def test_weight_gained_from_eating(self):

        for i in range(10):
            weight_herb = self.herb.weight + self.params_herb['beta']*i
            weight_carn = self.carn.weight + self.params_carn['beta']*i
            self.herb.weight_gained_from_eating(i)
            self.carn.weight_gained_from_eating(i)
            assert self.herb.weight == weight_herb
            assert self.carn.weight == weight_carn

    def test_lost_weight(self):
        weight_herb = self.herb.weight
        weight_carn = self.carn.weight
        for i in range(10):
            weight_herb = weight_herb - self.params_herb['eta']*weight_herb
            weight_carn = weight_carn - self.params_carn['eta']*weight_carn
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

    def test_birth_prob(self, mocker):
        """
        tests birth probabillty and birth weight
        """
        w_child = 8
        mocker.patch('random.random', return_value=0.78)  # set slightly lower than prob carn birth so birth happens
        mocker.patch('random.gauss', return_value=8)

        self.carn.calculate_fitness()

        self.herb.weight = 9.5  # smaller
        self.herb.calculate_fitness()
        new_born_herb = self.herb.birth(100)  # large N value to show that probabillity is zero
        assert new_born_herb == None

        self.herb.weight = 33
        self.herb.calculate_fitness()
        new_born_herb = self.herb.birth(100)  # large N value to show that probabillity is zero
        assert new_born_herb == None

        self.herb.weight = 34
        self.herb.calculate_fitness()
        new_born_herb = self.herb.birth(100)
        assert new_born_herb.age == 0
        assert new_born_herb.weight == 8

        self.carn.weight = 25# just bigger than one of the zero conditions for birth
        self.carn.calculate_fitness()

        new_born_carn = self.carn.birth(2)

        assert new_born_carn.weight == w_child
        assert new_born_carn.age == 0


    def test_death(self, mocker):
        """
        tests the death function so it works with
        """
        self.herb.calculate_fitness()
        mocker.patch('random.random', return_value=0.21)  # death prob = 20%
        self.herb.death()
        assert self.herb.is_dead == False

        mocker.patch('random.random', return_value=0.19)
        self.herb.death()
        assert self.herb.is_dead == True
        self.herb.is_dead == False

        self.herb.weight = 0
        self.herb.death()
        assert self.herb.is_dead == True

        self.carn.weight = 8  # makes death prob = 13.4%
        mocker.patch('random.random', return_value=0.14)
        self.carn.calculate_fitness()
        self.carn.death()
        assert self.carn.is_dead == False

        mocker.patch('random.random', return_value=0.12)
        self.carn.death()
        assert self.carn.is_dead == True
        self.carn.is_dead = False

        self.carn.weight = 0
        self.carn.death()
        assert self.carn.is_dead == True


    def test_carnivore_kill_prob(self):
        """
        tests the calculation of kill probabillity for predator
        """

        self.carn.fitness = 0.40
        self.herb.calculate_fitness()
        assert self.carn.carnivore_kill_prob(self.herb) == 0


        prob = (0.55- self.herb.fitness)/self.params_carn['DeltaPhiMax']
        self.carn.fitness = 0.55
        self.carn.carnivore_kill_prob(self.herb)

        assert self.carn.carnivore_kill_prob(self.herb) == pytest.approx(prob)



