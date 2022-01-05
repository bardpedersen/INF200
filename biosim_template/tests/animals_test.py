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

subject_herbivore = animals.Herbivore(1,40)
def reset_params(sub):
    sub.age = 1
    sub.weight = 40





def test_grow_one_year_test():
    """
    tests how good
    """

    subject_herbivore = animals.Herbivore(1, 40)
    age = 1
    for _ in range(10):
        subject_herbivore.grow_one_year()
        assert subject_herbivore.age == age + 1
        age += 1

def test_weight_gained_from_eating():

    for i in range(10):
        weight_real = 40 + beta*i
        subject_herbivore.weight_gained_from_eating(i)
        weight_func = subject_herbivore.weight
        assert weight_func == weight_real
        reset_params(subject_herbivore)

def test_weight_gained_from_eating():

    for i in range(10):
        weight_real = 40 + beta*i
        subject_herbivore.weight_gained_from_eating(i)
        weight_func = subject_herbivore.weight
        assert weight_func == weight_real
        reset_params(subject_herbivore)

def test_lost_weight():
    for i in range(10):
        weight_real = 40 - mu*40
        subject_herbivore.lose_weight()
        weight_func = subject_herbivore.weight
        assert weight_func == weight_real
        reset_params(subject_herbivore)