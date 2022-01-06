"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU

from biosim.animals import Herbivore
from biosim.landscapes import LowLand, Water
from biosim.island_map import Map

import matplotlib.pyplot as plt
import numpy as np


class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):

        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param vis_years: years between visualization updates (if 0, disable graphics)
        :param img_dir: String with path to directory for figures
        :param img_base: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. 'png'
        :param img_years: years between visualizations saved to files (default: vis_years)
        :param log_file: If given, write animal counts to this file

        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.

        If img_dir is None, no figures are written to file. Filenames are formed as

            f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'

        where img_number are consecutive image numbers starting from 0.

        img_dir and img_base must either be both None or both strings.
        """

        self._islandmap = island_map
        self.map = Map(island_map)
        self.ini_pop = ini_pop
        self.seed = seed
        self.vis_years = vis_years
        self._animal_species = {'Herbivore': Herbivore}
        self._landscape_types_changeable = {'L': LowLand}
        self._year = 0
        self._final_year = None
        self.x_list = []
        self.y_list = []

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species in self._animal_species:
            species_class = self._animal_species[species]
            animal = species_class()
            animal.set_params(params)
        else:
            raise TypeError(f'cannot assign parameters to {species} ')

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape in self._landscape_types_changeable:
            landscape_class = self._animal_species[landscape]
            land_type = landscape_class()
            landscape_class.cell_set_params()

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """

        self.map.creating_map()
        self.add_population(self.ini_pop)
        _final_year = self._year + num_years

        while self._year < num_years:
            self.map.island_feeding()
            self.map.island_procreation()
            self.map.island_migration()
            self.map.island_aging()
            self.map.island_weight_loss()
            self.map.island_death()
            self.update_graph_x()
            self.update_graph_y()
            self._year += 1

        self.make_graph()

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.map.island_add_population(population)

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """
        Total number of animals on island.
        """
        animals = 0
        for lanscape in self.map.map:
            animals += self.map.map[lanscape].cell_sum_of_herbivores()
        return animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        pass

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass

    def update_graph_x(self):
        self.x_list.append(self._year)
        return self.x_list

    def update_graph_y(self):
        self.y_list.append(self.num_animals)
        return self.y_list

    def make_graph(self):
        plt.plot(np.array(self.update_graph_x()), np.array(self.update_graph_y()))
        plt.xlabel('Years')
        plt.ylabel('Animals')
        plt.title('Herbivores in single cell')
        plt.show()
