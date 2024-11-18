import time
import numpy as np
import math
import matplotlib.pyplot as plt

class Fibonacci:
    def recursive(self, n):
        if n <= 1:
            return n
        else:
            return self.recursive(n-1) + self.recursive(n-2)

    def dynamicRecursive(self, n, cache={}):
        if n <= 1:
            return n
        elif n not in cache:
            cache[n] = self.dynamicRecursive(n-1, cache) + self.dynamicRecursive(n-2, cache)
        return cache[n]

    def iterative(self, n):
        if n <= 1:
            return n
        prev, curr = 0, 1
        for _ in range(n-1):
            prev, curr = curr, prev + curr
        return curr

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

# Define the range of n values
n_values = my_range = range(0, 10000, 50)

# Measure execution time for each method with normalization
max_time = 0
recursive_times, dynamic_recursive_times, iterative_times, matrix_times, binet_times, doubling_formula_times = [], [], [], [], [], []
for n in n_values:
    print(n)
    # start_time = time.time()
    # recursive_time = F.recursive(n)  # Measure recursive time
    # recursive_times.append(recursive_time)
    # max_time = max(max_time, time.time() - start_time)  # Update max

    start_time = time.time()
    dynamic_recursive_time = F.dynamicRecursive(n)
    dynamic_recursive_times.append(dynamic_recursive_time)
    max_time = max(max_time, time.time() - start_time)

    # start_time = time.time()
    # iterative_time = F.iterative(n)
    # iterative_times.append(iterative_time)
    # max_time = max(max_time, time.time() - start_time)

    # start_time = time.time()
    # matrix_time = F.matrix(n)
    # matrix_times.append(matrix_time)
    # max_time = max(max_time, time.time() - start_time)

    # start_time = time.time()
    # binet_time = F.binet(n)
    # binet_times.append(binet_time)
    # max_time = max(max_time, time.time() - start_time)

    # start_time = time.time()
    # doubling_formula_time = F.doublingFormula(n)
    # doubling_formula_times.append(doubling_formula_time)
    # max_time = max(max_time, time.time() - start_time)

# Normalize the times
# recursive_times_normalized = [t / max_time for t in recursive_times]
dynamic_recursive_times_normalized = [t / max_time for t in dynamic_recursive_times]
# iterative_times_normalized = [t / max_time for t in iterative_times]
# matrix_times_normalized = [t / max_time for t in matrix_times]
# binet_times_normalized = [t / max_time for t in binet_times]
# doubling_formula_times_normalized = [t / max_time for t in doubling_formula_times]

# Plotting
plt.figure(figsize=(10, 6))
# plt.plot(n_values, recursive_times_normalized, label='Recursive')
plt.plot(n_values, dynamic_recursive_times_normalized, label='Dynamic Recursive')
# plt.plot(n_values, iterative_times_normalized, label='Iterative')
# plt.plot(n_values, matrix_times_normalized, label='Matrix')
# plt.plot(n_values, binet_times_normalized, label='Binet')
# plt.plot(n_values, doubling_formula_times_normalized, label='Doubling Formula')

plt.xlabel('n')
plt.ylabel('Normalized Time')  
plt.title('Time Complexity of Fibonacci Calculation Methods')
plt.legend()
plt.grid(True)
plt.show()
