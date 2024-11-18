import numpy as np
import math

class Fibonacci:
    def recursive(self, n):
        if n <= 1:
            return n
        else:
            return self.recursive(n-1) + self.recursive(n-2)

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
        
    def iterative(self, n):
        if n <= 1:
            return n
        prev, curr = 0, 1
        for _ in range(n-1):
            prev, curr = curr, prev + curr
        return curr
    import numpy as np

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

    def binet(self, n):
        phi = (1 + math.sqrt(5)) / 2
        psi = (1 - math.sqrt(5)) / 2
        return int((phi**n - psi**n) / math.sqrt(5))
    
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
for i in range(6):
    print(F.recursive(i), F.dynamicRecursive(i), F.iterative(i), F.matrix(i), F.binet(i), F.doublingFormula(i))