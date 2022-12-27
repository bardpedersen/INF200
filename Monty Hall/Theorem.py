import random

number_of_games = 100000
right = 0
right_one_door = 0
right_monty = 0

for i in range(number_of_games):
    doors = ['a', 'b', 'c']
    right_answer = random.choice(doors)
    guess_one = random.choice(doors)
    wrong_answer = random.choice([door for door in doors if door not in (right_answer, guess_one)])

    # Without removing a door
    guess_two = random.choice(doors)

    # Without monty halls theorem
    _ = doors.remove(random.choice(wrong_answer))
    guess_with_one_less = random.choice(doors)

    # With monty halls theorem
    _ = doors.remove(guess_one)
    guess_monty = random.choice(doors)

    if right_answer == guess_two:
        right += 1

    if right_answer == guess_with_one_less:
        right_one_door += 1

    if right_answer == guess_monty:
        right_monty += 1

print(right/number_of_games)
print(right_one_door/number_of_games)
print(right_monty/number_of_games)
