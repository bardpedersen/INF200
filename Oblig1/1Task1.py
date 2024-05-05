dictionary = {}
with open('norway_municipalities_2017.csv', 'r') as f:
    header = f.readline().strip().split(',')
    for line in f:
        _, ds, p = line.split(',')
        dictionary[ds] = dictionary.get(ds, 0) + int(p)

print(f'{header[1]:20s}{header[2]:>s}')
print(30*'-')
for ds, p in sorted(dictionary.items(), key=lambda s: s[1], reverse=True):
    print(f'{ds:20s}{p:10d}')

