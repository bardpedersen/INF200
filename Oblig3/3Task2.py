import re

file = ["Ali and Per and friends.", "Kari and Joe know each other.", "James has know Peter since school days."]
navn = []
for i in file:
    m = re.findall(r"([A-Z][a-z]+)", i)
    navn.append(m)
print(f"{'Friendship':^24s}")
print(f"{'-'*24:^24s}")
for i, j in enumerate(navn):
    print(f"{navn[i][0]:>10}{'-':^3s}{navn[i][1]:<10}")

