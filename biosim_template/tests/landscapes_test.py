from biosim.landscapes import OneGrid, Water, Lowland, Highland, Dessert
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

low = Lowland()
high = Highland()
des = Dessert()
water = Water()

def reset_varibels():
    start_nr_animals = None
    end_nr_animals = None
    fodder_before = None
    fodder_after = None
    weight_before = None
    weight_after = None
    fodder_grows = None

"""Testing in Lowland"""
def test_add_population():
    """
    Test that adding animals works.
    """
    pop = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(100)]
    start_nr_animals = low.cell_sum_of_herbivores()
    low.cell_add_population(pop)
    end_nr_animals = low.cell_sum_of_herbivores()

    assert start_nr_animals == 0
    assert end_nr_animals == 100

def test_remove_population():
    """
    Test that removing/dead animals work
    """
    start_nr_animals = low.cell_sum_of_herbivores()
    dead_pop = [{'species': 'Herbivore', 'age': 5, 'weight': 0} for _ in range(10)]
    low.cell_add_population(dead_pop)
    dead_nr_animals = low.cell_sum_of_herbivores()
    low.cell_death()
    end_nr_animals = low.cell_sum_of_herbivores()

    assert start_nr_animals == 100
    assert dead_nr_animals == 110
    assert end_nr_animals < 100


def test_feeding():
    """
    Testing that growing food as well ass feeding works
    """
    low.cell_add_fodder()
    fodder_before = low.fodder
    weight_list_before = []
    for animal in low.population_herb:
        weight_list_before.append(animal.weight)
    weight_before = sum(weight_list_before)/len(weight_list_before)

    low.cell_feeding_herbivore()
    fodder_after = low.fodder
    weight_list_after = []
    for animal in low.population_herb:
        weight_list_after.append(animal.weight)
    weight_after = sum(weight_list_after)/len(weight_list_after)

    low.cell_add_fodder()
    fodder_grows = low.fodder
    nr_animals = low.cell_sum_of_herbivores()
    assert fodder_before == 800
    assert fodder_after == 800 - (nr_animals * 10)
    assert weight_before == 20
    assert weight_after == weight_before + beta * 10
    assert fodder_grows == 800

def procreation():
    pass

def test_Highland():
    reset_varibels()

    pop = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(15)]
    start_nr_animals = high.cell_sum_of_herbivores()
    high.cell_add_population(pop)
    end_nr_animals = high.cell_sum_of_herbivores()

    high.cell_add_fodder()
    fodder_before = high.fodder
    weight_list_before = []
    for animal in high.population_herb:
        weight_list_before.append(animal.weight)
    weight_before = sum(weight_list_before)/len(weight_list_before)

    high.cell_feeding_herbivore()
    fodder_after = high.fodder
    weight_list_after = []
    for animal in high.population_herb:
        weight_list_after.append(animal.weight)
    weight_after = sum(weight_list_after)/len(weight_list_after)

    high.cell_add_fodder()
    fodder_grows = high.fodder
    nr_animals = high.cell_sum_of_herbivores()
    assert start_nr_animals == 0
    assert end_nr_animals == 15
    assert fodder_before == 300
    assert fodder_after == 300 - (nr_animals * 10)
    assert weight_before == 20
    assert weight_after == weight_before + beta * 10
    assert fodder_grows == 300

def test_Dessert():
    reset_varibels()

    pop = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(15)]
    start_nr_animals = des.cell_sum_of_herbivores()
    des.cell_add_population(pop)
    end_nr_animals = des.cell_sum_of_herbivores()

    des.cell_add_fodder()
    fodder_before = des.fodder
    weight_list_before = []
    for animal in des.population_herb:
        weight_list_before.append(animal.weight)
    weight_before = sum(weight_list_before) / len(weight_list_before)

    des.cell_feeding_herbivore()
    fodder_after = des.fodder
    weight_list_after = []
    for animal in des.population_herb:
        weight_list_after.append(animal.weight)
    weight_after = sum(weight_list_after) / len(weight_list_after)

    des.cell_add_fodder()
    fodder_grows = des.fodder
    nr_animals = des.cell_sum_of_herbivores()
    assert start_nr_animals == 0
    assert end_nr_animals == 15
    assert fodder_before == 0
    assert fodder_after == 0
    assert weight_before == 20
    assert weight_after == 20
    assert fodder_grows == 0

def test_Water():
    reset_varibels()

    pop = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(15)]
    start_nr_animals = water.cell_sum_of_herbivores()
    water.cell_add_population(pop)
    end_nr_animals = water.cell_sum_of_herbivores()

    water.cell_add_fodder()
    fodder_before = water.fodder
    weight_list_before = []
    if len(weight_list_before) != 0:
        for animal in water.population_herb:
            weight_list_before.append(animal.weight)
        weight_before = sum(weight_list_before) / len(weight_list_before)
    else:
        weight_before = 0

    water.cell_feeding_herbivore()
    fodder_after = water.fodder
    weight_list_after = []
    if len(weight_list_before) != 0:
        for animal in water.population_herb:
            weight_list_after.append(animal.weight)
        weight_after = sum(weight_list_after) / len(weight_list_after)
    weight_after = 0

    water.cell_add_fodder()
    fodder_grows = water.fodder
    nr_animals = water.cell_sum_of_herbivores()
    assert start_nr_animals == 0
    assert end_nr_animals == 0
    assert fodder_before == 0
    assert fodder_after == 0
    assert weight_before == 0
    assert weight_after == 0
    assert fodder_grows == 0
