def selection_pythonic(a):
    n = len(a)
    for i in range(n-1):
        min_index = min(range(i, n), key = lambda x: a[x])
        a[min_index], a[i] = a[i], a[min_index]
    return a

def selection_normal(a):
    n = len(a)
    counter = 0
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            counter += 1
            if a[j] < a[min_index]:
                min_index = j
        if min_index != i:
            a[min_index], a[i] = a[i], a[min_index]
    return counter, a

def selection_cringe(a):
    n = len(a)
    for i in range(n-1):
        for j in range(i+1, n):
            if a[j] < a[i]:
                a[j], a[i] = a[i], a[j]
    return a
        

a = [10,1,24,6,7,43,2,6,76,7,43,2,6]

print(selection_pythonic(a.copy()))
print(selection_normal(a.copy()))
print(selection_cringe(a.copy()))
print(a)