def letter_freq(txt):
    freq = {}
    for char in set(txt):
        freq[char] = txt.count(char)
    return freq


if __name__ == '__main__':
    text = input('Please enter text to analyse: ')

    frequencies = letter_freq(text)
    for letter, count in frequencies.items():
        print('{:3}{:10}'.format(letter, count))
