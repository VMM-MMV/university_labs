a = [10,1,24,6,7,43,2,6,76,7,43,2,6]

def mergeSort(a):
    if len(a) == 1:
        return
        
    mid = len(a) // 2
    left_a = a[:mid]
    right_a = a[mid:]
    mergeSort(left_a)
    mergeSort(right_a)
    merge(a, left_a, right_a)
    return a

def merge(a, left_a, right_a):
    i,l,r = 0,0,0
    len_left = len(left_a)
    len_right = len(right_a)
    while l < len_left and r < len_right:
        if left_a[l] < right_a[r]:
            a[i] = left_a[l]
            l += 1
        else:
            a[i] = right_a[r]
            r += 1
        i += 1

    while l < len_left:
        a[i] = left_a[l]
        l += 1
        i += 1

    while r < len_right:
        a[i] = right_a[r]
        r += 1
        i += 1

s = mergeSort(a.copy())
print(a)
print(s)
