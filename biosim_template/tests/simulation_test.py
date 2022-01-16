from biosim.simulation import BioSim
import pytest
import textwrap

class TestSimulation:

    @pytest.fixture(autouse=True)
    def settup_simulation(self):
        island_map = """\
           WWW
           WLW
           WWW"""
        island_map = textwrap.dedent(island_map)
        self.seed = 123
        self.pop = [{'loc': (2, 2),
                     'pop': [{'species': 'Herbivore',
                              'age': 5,
                              'weight': 20}
                             for _ in range(20)]}]
        self.biosim = BioSim(island_map=island_map, ini_pop=self.pop, seed=self.seed)

    def test_population_start(self):
        assert self.biosim.num_animals == 0

    def test_population_after_one_year(self):
        self.biosim.add_population(self.pop)
        self.biosim.simulate(1)
        assert self.biosim.num_animals == 20

    def test_year_zero(self):
        assert self.biosim.year == 0


    def test_set_animal_parameters(self):
        pass

    def test_set_landscape_parameters(self):
        pass

    def test_simulate(self):
        pass


    def test_num_animals_per_species(self):
        pass

    def test_setup_logfile(self):
        pass

    def test_save_to_file(self):
        pass

    def test_make_movie(self):
        pass

