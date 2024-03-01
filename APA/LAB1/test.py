import numpy as np
import math
from line_profiler import LineProfiler

class Fibonacci:
    def __init__(self):
        pass

    @profile
    def recursive(self, n):
        if n <= 1:
            return n
        else:
            return self.recursive(n-1) + self.recursive(n-2)

    @profile
    def dynamicRecursive(self, n):
        cache = {}
        def recursive(n):
            if n in cache:
                return cache[n]
            if n <= 1:
                return n
            cache[n] = recursive(n-1) + recursive(n-2)

            return cache[n]
        return recursive(n)

    @profile
    def iterative(self, n):
        if n <= 1:
            return n
        prev, curr = 0, 1
        for _ in range(n-1):
            prev, curr = curr, prev + curr
        return curr

    @profile
    def matrix(self, n):
        if n <= 1:
            return n

        base_matrix = np.array([[1, 1], [1, 0]], dtype=object)
        
        def matrix_power(matrix, power):
            result = np.eye(2, dtype=object)
            while power > 0:
                if power % 2 == 1:
                    result = np.dot(result, matrix)
                matrix = np.dot(matrix, matrix)
                power //= 2
            return result
        
        result_matrix = matrix_power(base_matrix, n - 1)
        return result_matrix[0][0]

    @profile
    def binet(self, n):
        phi = (1 + math.sqrt(5)) / 2
        psi = (1 - math.sqrt(5)) / 2
        return int((phi**n - psi**n) / math.sqrt(5))

    @profile
    def doublingFormula(self, n):
        if n <= 1:
            return n
        def fib(n):
            if n == 0:
                return 0, 1
            a, b = fib(n // 2)
            c = a * (2 * b - a)
            d = a * a + b * b
            if n % 2 == 0:
                return c, d
            else:
                return d, c + d
        return fib(n)[0]

F = Fibonacci()
lp = LineProfiler()
lp.add_function(F.recursive)
lp.add_function(F.dynamicRecursive)
lp.add_function(F.iterative)
lp.add_function(F.matrix)
lp.add_function(F.binet)
lp.add_function(F.doublingFormula)

for i in range(6):
    lp_wrapper = lp(F.recursive)
    lp_wrapper(i)
    lp_wrapper = lp(F.dynamicRecursive)
    lp_wrapper(i)
    lp_wrapper = lp(F.iterative)
    lp_wrapper(i)
    lp_wrapper = lp(F.matrix)
    lp_wrapper(i)
    lp_wrapper = lp(F.binet)
    lp_wrapper(i)
    lp_wrapper = lp(F.doublingFormula)
    lp_wrapper(i)

lp.print_stats()
