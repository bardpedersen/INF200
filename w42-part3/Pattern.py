import time

while True:
    """
    loop that prints the pattern
    The reversed variables is for printing the upside down verson of the pattern 
    """
    spaces = 21
    hashtags = 0
    counter = 0
    stars = 1
    spaces_reversed = 1
    hashtags_reversed = 20
    counter_reversed = 20
    while counter != 20:
        """
        While loop that prints the upper part of the pattern
        """
        print((spaces *' ' + stars *'*' + 2 * hashtags *'#' + stars *'*' + spaces *' ' + spaces_reversed * ' ' + stars * '*' + 2 * hashtags_reversed * '#' + stars * '*' + spaces_reversed * ' ') * 3)
        spaces -= 1
        hashtags += 1
        counter += 1
        time.sleep(0.4)
        spaces_reversed += 1
        hashtags_reversed -= 1
        counter_reversed -= 1
    while counter != 0:
        """
        Loop that prints the lower part of the pattern
        """
        print((spaces *' ' + stars *'*' + 2 * hashtags *'#' + stars *'*' + spaces *' ' + spaces_reversed * ' ' + stars * '*' + 2 * hashtags_reversed * '#' + stars * '*' + spaces_reversed * ' ') * 3)
        spaces += 1
        hashtags -= 1
        counter -= 1
        time.sleep(0.4)
        spaces_reversed -= 1
        hashtags_reversed += 1
        counter_reversed += 1

