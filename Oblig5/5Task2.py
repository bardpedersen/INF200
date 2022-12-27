__author__ = 'Bård'
__email__ = 'bard.tollef.pedersen@nmbu.no'

from random import randint as rand


def yourGuess():
    count = 0
    while count < 1:
        count = int(input('Your guess: '))
    return count


def diceThrow():
    return rand(1, 6) + rand(1, 6)


def controll(ans, guess):
    return ans == guess


if __name__ == '__main__':

    win = False
    score = 3
    corAnsw = diceThrow()
    while not win and score > 0:
        yourAnsw = yourGuess()
        win = controll(corAnsw, yourAnsw)
        if not win:
            print('Wrong, try again!')
            score -= 1

    if score > 0:
        print('You won {} points.'.format(score))
    else:
        print('You lost. Correct answer: {}.'.format(corAnsw))
