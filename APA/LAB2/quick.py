a = [10,1,24,8,6,7,43,76,9,7]

def quickSort(a, low, high):
    if low < high:
        pivit_pos = sortByPivot(a, low, high)
        quickSort(a, low, pivit_pos - 1)
        quickSort(a, pivit_pos+1, high)

def sortByPivot(a, low, high):
    i = low - 1
    for j in range(low, high):
        if a[j] <= a[high]:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i+1], a[high] = a[high], a[i+1]
    return i

quickSort(a, 0, len(a)-1)
print(a)