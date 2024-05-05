def bubble_sort(data):
    order = list(data)
    leng = len(order)

    for i in range(leng-1):
        for j in range(0, leng-i-1):
            if order[j] > order[j + 1]:
                order[j], order[j + 1] = order[j + 1], order[j]
    return order


if __name__ == "__main__":
    for data in ((),
                 (1,),
                 (1, 3, 8, 12),
                 (12, 8, 3, 1),
                 (8, 3, 12, 1)):
        print('{!s:>15} --> {!s:>15}'.format(data, bubble_sort(data)))
