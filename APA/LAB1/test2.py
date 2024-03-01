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

    # def matrix(self, n):
    #     """Calculates the nth Fibonacci number using matrix exponentiation"""
    #     def multiply(matrix_a, matrix_b):
    #         """Multiplies two 2x2 matrices"""
    #         result = [[0, 0], [0, 0]]
    #         for i in range(2):
    #             for j in range(2):
    #                 for k in range(2):
    #                     result[i][j] += matrix_a[i][k] * matrix_b[k][j]
    #         return result

    #     def matrix_power(matrix, n):
    #         """Calculates the nth power of a 2x2 matrix"""
    #         if n == 0:
    #             return [[1, 0], [0, 1]]  # Identity matrix
    #         elif n == 1:
    #             return matrix
    #         else:
    #             half_power = matrix_power(matrix, n // 2)
    #             if n % 2 == 0:
    #                 return multiply(half_power, half_power)
    #             else:
    #                 return multiply(multiply(half_power, half_power), matrix) 
    #     if n < 0:
    #         print("Invalid input: n must be non-negative")
    #         return None
    #     elif n <= 1:
    #         return n
    #     else:
    #         fibonacci_matrix = [[1, 1], [1, 0]]
    #         result_matrix = matrix_power(fibonacci_matrix, n - 1)
    #         return result_matrix[0][0]
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
n_values = my_range = range(0, 44, 2)

# Measure execution time for each method
recursive_times = []
dynamic_recursive_times = []
iterative_times = []
matrix_times = []
binet_times = []
doubling_formula_times = []

for n in n_values:
    print(n)
    start_time = time.time()
    F.recursive(n)
    recursive_times.append(time.time() - start_time)

    # start_time = time.time()
    # F.dynamicRecursive(n)
    # dynamic_recursive_times.append(time.time() - start_time)

    # start_time = time.time()
    # F.iterative(n)
    # iterative_times.append(time.time() - start_time)

    # start_time = time.time()
    # F.matrix(n)
    # matrix_times.append(time.time() - start_time)

    # start_time = time.time()
    # F.binet(n)
    # binet_times.append(time.time() - start_time)

    # start_time = time.time()
    # F.doublingFormula(n)
    # doubling_formula_times.append(time.time() - start_time)

def find_max_last_value(lists):
  max_last_value = None
  for lst in lists:
    if lst:
      last_value = lst[-1]
      if max_last_value is None or last_value > max_last_value:
        max_last_value = last_value

  return max_last_value

all_lists = [recursive_times, dynamic_recursive_times, iterative_times, 
             matrix_times, binet_times, doubling_formula_times]

# Find the maximum last value
max_value = find_max_last_value(all_lists)


# Plotting
plt.figure(figsize=(10, 6))
plt.plot(n_values, recursive_times, label='Recursive')
# plt.plot(n_values, dynamic_recursive_times, label='Dynamic Recursive')
# plt.plot(n_values, iterative_times, label='Iterative')
# plt.plot(n_values, matrix_times, label='Matrix')
# plt.plot(n_values, binet_times, label='Binet')
# plt.plot(n_values, doubling_formula_times, label='Doubling Formula')

# plt.ylim(0, max_value*1.1) 
plt.xlabel('n')
plt.ylabel('Time (seconds)')
plt.title('Time Complexity of Fibonacci Calculation Methods')
plt.legend()
plt.grid(True)
plt.show()
