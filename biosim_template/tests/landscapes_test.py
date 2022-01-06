from biosim import landscapes
from biosim import animals
import pytest

w_birth = 8.0
sigma_birth = 1.5
beta = 0.9
eta = 0.05
a_half = 40.0
phi_age = 0.6
w_half = 10.0
phi_weight = 0.1
mu = 0.25
gamma = 0.2
zeta = 3.5
xi = 1.2
omega = 0.4
F = 10

low = landscapes.LowLand()
herb = animals.Herbivore(age = 0, weight = 0)

def test_add_population():
    """
    Test that adding animals works.
    """
    pop = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(100)]
    start_nr_animals = low.sum_of_herbivores()
    low.add_population(pop)
    end_nr_animals = low.sum_of_herbivores()

    assert start_nr_animals == 0
    assert end_nr_animals == 100

def test_remove_population():
    """
    Test that removing/dead animals work
    """
    start_nr_animals = low.sum_of_herbivores()
    dead_pop = [{'species': 'Herbivore', 'age': 5, 'weight': 0} for _ in range(10)]
    low.add_population(dead_pop)
    dead_nr_animals = low.sum_of_herbivores()
    low.calculate_fitness_in_cell()
    low.death_in_cell()
    end_nr_animals = low.sum_of_herbivores()

    assert start_nr_animals == 100
    assert dead_nr_animals == 110
    assert end_nr_animals < 100


def test_feeding():
    """
    Testing that growing food as well ass feeding works
    """
    low.add_fooder()
    fodder_before = low.fodder
    weight_list_before = []
    for animal in low.population_herb:
        weight_list_before.append(animal.weight)
    weight_before = sum(weight_list_before)/len(weight_list_before)

    low.feeding()
    fodder_after = low.fodder
    weight_list_after = []
    for animal in low.population_herb:
        weight_list_after.append(animal.weight)
    weight_after = sum(weight_list_after)/len(weight_list_after)

    low.add_fooder()
    fodder_grows = low.fodder
    assert fodder_before == 800
    assert fodder_after == 140
    assert weight_before == 20
    assert weight_after == weight_before + beta * 10
    assert fodder_grows == 800
