#Valgdistrikt
#Mandat 2020-2028
with open('seats_per_district.txt') as f:
    lines = f.readlines()  #
    for i, line in enumerate(lines):
        if 'Østfold' in line:
            break
    for j, line in enumerate(lines):
        if 'Finnmark' in line:
            break
    trimmedText = lines[i:j+5]
    newTextList = []
    for element in trimmedText:
        newTextList.append(element.strip())
    newTextList = list(filter(None, newTextList))
    valgdistrikt = newTextList[::5]
    newTextList2 = newTextList
    for i in range(3):
        newTextList2.pop(i)
    newTextList2.pop(0)
    mandat = newTextList2[::5]
    dictonary = dict(zip(valgdistrikt, mandat))
print(30*'-')
for valgdistrikt, mandat in sorted(dictonary.items()):
    print(f'{valgdistrikt:20s}{mandat:20s}')
