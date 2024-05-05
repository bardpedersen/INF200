def valg2021(file, antallparti=0):
    dictionary = {}
    totalstemmer = 0
    with open(file, 'r') as f:
        header = f.readline().strip().split(';')
        for line in f:
            lines = line.split(';')
            parti = lines[6]
            stemmer = lines[12]
            totalstemmer = totalstemmer + int(stemmer)
            dictionary[parti] = dictionary.get(parti, 0) + int(stemmer)

    a = 'Porsent'
    print(f'{header[6]:15s}{header[12]:25s}{a}')
    print(55 * '-')
    if antallparti == 0:
        for parti, stemmer in sorted(dictionary.items(), key=lambda s: s[1], reverse=True):
            prosent = float(stemmer / totalstemmer)
            if prosent > 0.04:
                a = f'{parti:20s}{str(stemmer):20s}{prosent:.2%}'
                print('\x1b[6;30;42m' + a + '\x1b[0m')
            else:
                print(f'{parti:20s}{str(stemmer):20s}{prosent:.2%}')
    else:
        for parti, stemmer in sorted(dictionary.items(), key=lambda s: s[1], reverse=True)[:antallparti]:
            prosent = float(stemmer / totalstemmer)
            if prosent > 0.04:
                a = f'{parti:20s}{str(stemmer):20s}{prosent:.2%}'
                print('\x1b[6;30;42m' + a + '\x1b[0m')
            else:
                print(f'{parti:20s}{str(stemmer):20s}{prosent:.2%}')


valg2021('2021-09-14_party distribution_1_st_2021.csv', 9)
