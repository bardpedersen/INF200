from biosim import animals

test_subject_herbivore = animals.Herbivore(1,40)

def grow_one_year_test():
    n = 10
    for _ in range(n):
        test_subject_herbivore.grow_one_year()
        assert test_subject_herbivore.age == n +1

