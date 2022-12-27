import re

text = "I can see the the red rose rose and the the purple lilac."
print(text)
ord_ferdig=0
for m in re.finditer(r"\b(\w+)\s+\1\b", text):
    dash = m.start() - ord_ferdig
    star = m.end() - m.start()
    print(' '* dash + '*' * star, end='')
    ord_ferdig = m.end()
