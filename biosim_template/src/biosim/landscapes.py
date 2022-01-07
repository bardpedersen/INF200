from biosim.animals import Herbivore,Carnivore
import random as rd


class OneGrid:
    seed = 12345
    params = {
        'f_max_Lowland': 800,
        'f_max_Highland': 300
        }

    def __init__(self):
        self.fodder = 0
        self.population_herb = []
        self.population_carn = []
        self.population_sum = None
        self.livable = True

    def __repr__(self):
        return f'Lowland,Food:{self.fodder},Total animals:{self.population_sum}'

    def cell_set_params(cls, params):
        for parameter in params:
            if parameter in cls.params:
                cls[parameter] = params[parameter]

    def cell_add_population(self, population=None):
        """
        adds a population to the landscape location, and turns it in to an animal object
        :param population: the population to add to the map
        :return:
        """

        for animal in population:
            if animal['species'] == 'Herbivore':
                self.population_herb.append(Herbivore(animal['age'], animal['weight']))
            elif animal['species'] == 'Carnivore':
                self.population_carn.append(Carnivore(animal['age'], animal['weight']))

    def cell_sum_of_herbivores(self):
        self.population_sum = len(self.population_herb)
        return self.population_sum

    def cell_calculate_fitness(self):
        """
        uses the calculate fitness function from animals
        to calculate the fitness of each animal in cell
        :return:
        """

        for animal in self.population_herb:
            animal.calculate_fitness()

        for animal in self.population_carn:
            animal.calculate_fitness()

    def cell_add_fodder(self):
        self.fodder = 800

    def cell_feeding_herbivore(self):
        """
        Animals residing in a cell eat in descend- ing order of fitness.
        Each animal tries every year to eat an amount F of fodder,
        but how much feed the animal obtain depends on fodder available in the cell
        this function also sets the fooder for
        """

        self.cell_calculate_fitness()
        self.population_herb.sort(key=lambda x: x.fitness, reverse=True)
        for herbivore in self.population_herb:
            if self.fodder == 0:
                break
            elif self.fodder >= herbivore.params['F']:
                herbivore.weight_gained_from_eating(herbivore.params['F'])
                self.fodder = self.fodder - herbivore.params['F']
            elif 0 < self.fodder < herbivore.params['F']:
                herbivore.weight_gained_from_eating(self.fodder)
                self.fodder = 0

    def cell_feeding_carnivore(self):
        pass
        self.cell_calculate_fitness()
        self.population_herb.sort(key=lambda x: x.fitness, reverse=True)

        self.cell_calculate_fitness()
        rd.shuffle(self.population_carn)
        for predator in self.population_carn:
            amount_eaten = 0
            if amount_eaten == predator.params['F']:
                for prey in self.population_herb:
                    prob = predator.carnivore_kill_prob(prey)
                    if rd.random() < prob:
                        predator.carnivore_weight_gained_eating(prey)

    def cell_procreation(self):
        """
        Animals can mate if there are at least two animals of the same species in a cell.
        Gender plays no role in mating.Each animal can give birth to at most one off- spring per year.
        At birth, the mother animal loses ξ times the actual birth weight of the baby.
        If the mother would lose more than her own weight,
        then no baby is born and the weight of the mother remains unchanged.
        """
        new_borns = []
        N = self.population_sum
        for animal in self.population_herb:
            animal.calculate_fitness()
            new_born = animal.birth(N)
            if new_born is not None:
                new_borns.append(new_born)
            N -= 1
        self.population_herb += new_borns  # adds the newborns to the population at the end

    def cell_migration(self):
        """No migration on one cell island"""
        pass

    def cell_aging(self):
        """
        At birth, each animal has age a = 0 .
        Age increases by one year for each year that passes
        """
        for animal in self.population_herb:
            animal.grow_one_year()

    def cell_weight_lost(self):
        """
        Every year, the weight of the animal decreases.
        """
        for animal in self.population_herb:
            animal.lose_weight()

    def cell_death(self):
        """
        Animals die when its weight is w = 0 or
        by probability
        """
        self.cell_calculate_fitness()
        kill_list = []
        for animal in self.population_herb:
            if animal.death():
                index_death = self.population_herb.index(animal)
                kill_list.append(index_death)
        for i in sorted(kill_list, reverse=True):
            del self.population_herb[i]


class Lowland(OneGrid):
    def __init__(self):
        super().__init__()
        self._fodder = 800

    def __repr__(self):
        return f'Lowland,Food:{self._fodder},Total animals:{self.population_sum}'


class Highland(OneGrid):
    def __init__(self):
        super().__init__()
        self._fodder = 300

    def __repr__(self):
        return f'Highland,Food:{self._fodder},Total animals:{self.population_sum}'


class Dessert(OneGrid):
    def __init__(self):
        super().__init__()
        self._fodder = None

    def __repr__(self):
        return f'Dessert,Food:{self._fodder},Total animals:{self.population_sum}'


class Water(OneGrid):
    def __init__(self):
        super().__init__()
        self._fodder = None
        self.livable = False

    def __repr__(self):
        return f'Water,Food:{self._fodder},Uninhabitable'
