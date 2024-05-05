def head(file, n=5):
    with open(file,'r') as f:
        for line in (f.readlines()[:n]):
            print(line.rstrip('\n'))

def tail(file, n=5):
    with open(file,'r') as f:
        for line in (f.readlines()[-n:]):
            print(line.rstrip('\n'))

head('norway_municipalities_2017 copy.csv')
tail('norway_municipalities_2017 copy.csv')
