"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU

from biosim.animals import Herbivore, Carnivore
from biosim.landscapes import Lowland, Highland
from biosim.island_map import Map
from biosim.visualization import Visualization

import random as rd
import textwrap


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
        rd.seed(seed)
        self.island_map = textwrap.dedent(island_map)
        self.ini_pop = ini_pop
        self.vis_years = vis_years
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.img_dir = img_dir
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.img_years = img_years
        self.log_file = log_file
        self._year = 0
        self._final_year = None
        self._animal_species = {'Herbivore': Herbivore, 'Carnivore': Carnivore}
        self._landscape_types_changeable = {'L': Lowland, 'H': Highland}
        self.map = Map(self.island_map)
        self.map.creating_map()
        self.visual = Visualization(self.img_dir, self.img_base, self.img_fmt)

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
            landscape_class = self._landscape_types_changeable[landscape]
            land_type = landscape_class()
            land_type.cell_set_params(params)

    def simulate(self, num_years, vis_steps=1, img_steps=None):
        """
        Run simulation while visualizing the result.
        :param img_steps: number of steps to save image
        :param num_years: number of years to simulate
        :param vis_steps:
        """

        self.add_population(self.ini_pop)
        if img_steps is None:
            img_steps = vis_steps
        if img_steps % vis_steps != 0:
            raise ValueError('img_steps must be multiple of vis_steps')
        self._final_year = self._year + num_years
        self.visual.setup(self.map, self._final_year, self.ymax_animals)

        while self._year < self._final_year:
            self.map.island_update_one_year()
            if self._year % vis_steps == 0:
                self.visual.update(self._year,self.map,self.cmax_animals,self.hist_specs,self.ymax_animals)
            if self.log_file is not None:
                self.save_to_file()

            self._year += 1

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
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.
        """
        self.map.island_total_sum_of_animals()
        herb = self.map.island_total_herbivores
        if herb is None:
            herb = 0
        carn = self.map.island_total_carnivores
        if carn is None:
            carn = 0
        return {'Herbivore': herb, 'Carnivore': carn}

    @property
    def num_animals(self):
        """
        Total number of animals on island.
        """

        pop = self.map.island_total_sum_of_animals()
        if pop is None:
            pop = 0

        return pop

    def setup_logfile(self):
        """
        Writes the first line to logfile
        """
        logfile = open(self.log_file, "w")
        logfile.write("Year,Total_Herbivores,Total_Carnivores\n")
        logfile.close()

    def save_to_file(self):
        """
        Writes year, total herbivores and total carnivores to file
        """
        logfile = open(self.log_file, "a")
        logfile.write(f"{self._year},{self.map.island_total_herbivores},{self.map.island_total_carnivores}\n")
        logfile.close()

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        self.visual.make_movie()
