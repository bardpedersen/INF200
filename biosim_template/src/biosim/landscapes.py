from biosim.animals import Herbivore,Carnivore
import random as rd


class OneGrid:
    seed = 12345
    rd.seed(12345)

    def __init__(self):
        self.fodder = 0
        self.population_herb = []
        self.population_carn = []
        self.population_sum_herb = None
        self.population_sum_carn = None




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


    def cell_sum_of_animals(self):
        self.population_sum_herb = len(self.population_herb)
        self.population_sum_carn = len(self.population_carn)


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
        self.fodder = self.params['f_max']

    def cell_feeding_herbivore(self):
        """
        Animals residing in a cell eat in descend- ing order of fitness.
        Each animal tries every year to eat an amount F of fodder,
        but how much feed the animal obtain depends on fodder available in the cell
        this function also sets the fooder for

        Here:
        F = 10
        f_max = 800
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
        """
        implements feeding of carniores for the cell
        """
        self.cell_calculate_fitness()
        self.population_herb.sort(key=lambda x: x.fitness, reverse=True)

        self.cell_calculate_fitness()

        rd.shuffle(self.population_carn)
        for predator in self.population_carn:
            appetite = predator.params['F']
            amount_eaten = 0

            for prey in self.population_herb:
                prob = predator.carnivore_kill_prob(prey)
                if rd.random() < prob:
                    fodder = prey.weight
                    if amount_eaten + fodder < appetite:
                        prey.is_dead = True
                        predator.carnivore_weight_gained_eating(fodder)
                        amount_eaten += fodder
                    elif amount_eaten + fodder > appetite:
                        prey.is_dead = True
                        fodder = appetite - amount_eaten
                        predator.carnivore_weight_gained_eating(fodder)
                        break
                    elif amount_eaten + fodder == appetite:
                        prey.is_dead = True
                        predator.carnivore_weight_gained_eating(fodder)
                        break
                    predator.calculate.fitness()
            population_herb = [herb for herb in self.population_herb if herb.is_dead == False]
            self.population_herb = population_herb



    def cell_procreation(self):
        """
        Animals can mate if there are at least two animals of the same species in a cell.
        Gender plays no role in mating.Each animal can give birth to at most one off- spring per year.
        At birth, the mother animal loses ξ times the actual birth weight of the baby.
        If the mother would lose more than her own weight,
        then no baby is born and the weight of the mother remains unchanged.
        """
        self.cell_sum_of_animals()
        new_born_herbs = []
        N_H = self.population_sum_herb
        for herb in self.population_herb:
            herb.calculate_fitness()
            new_born_herb = herb.birth(N_H)
            if new_born_herb is not None:
                new_born_herbs.append(new_born_herb)
            N_H -= 1
        self.population_herb += new_born_herbs

        new_born_carns = []
        N_C = self.population_sum_carn
        for carn in self.population_carn:
            carn.calculate_fitness()
            new_born_carn = carn.birth(N_C,species='carn')
            if new_born_carn is not None:
                new_born_carns.append(new_born_carn)
            N_C -= 1
        self.population_carn += new_born_carns

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
        This func kills and removes both carnivores and herbivores in each cell
        """
        self.cell_calculate_fitness()
        for herb in self.population_herb:
            herb.death()
        for carn in self.population_carn:
            carn.death()

        population_herb = [herb for herb in self.population_herb if herb.is_dead == False]
        self.population_herb = population_herb
        population_carn = [carn for carn in self.population_carn if carn.is_dead == False]
        self.population_carn = population_carn



class Lowland(OneGrid):
    params = {
        'f_max': 800
    }
    def __init__(self):
        super().__init__()
        self._fodder = 800
        self.livable = True

    def __repr__(self):
        return f'Lowland,Food:{self.fodder},Total animals:{self.population_sum_carn+ self.population_sum_herb}'


class Highland(OneGrid):
    params = {
        'f_max': 300
    }
    def __init__(self):
        super().__init__()
        self.fodder = 0
        self.livable = True

    def __repr__(self):
        return f'Highland,Food:{self.fodder},Total animals:{self.population_sum_carn+ self.population_sum_herb}'


class Dessert(OneGrid):
    def __init__(self):
        super().__init__()
        self.fodder = 0
        self.livable = True

    def __repr__(self):
        return f'Dessert,Food:{self.fodder},Total animals:{self.population_sum_herb +self.population_sum_carn}'


class Water(OneGrid):
    def __init__(self):
        super().__init__()
        self._fodder = 0
        self.livable = False

    def __repr__(self):
        return f'Water,Food:{self._fodder},Uninhabitable'


    def cell_add_fodder(self):
        pass