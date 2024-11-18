import numpy as np
import math
from Fibonacci import Fibonacci  # Assuming your Fibonacci class is defined in a module called fibonacci.py
from line_profiler import LineProfiler
import matplotlib.pyplot as plt

# Create an instance of Fibonacci class
F = Fibonacci()

# Create a LineProfiler instance
lp = LineProfiler()

# Add the functions you want to profile
lp.add_function(F.recursive)
lp.add_function(F.dynamicRecursive)
lp.add_function(F.iterative)
lp.add_function(F.matrix)
lp.add_function(F.binet)
lp.add_function(F.doublingFormula)

# Define a function to run profiling and collect statistics
def run_profiling():
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

# Run profiling
run_profiling()

# Get profiling statistics
stats = lp.get_stats()

# Plot the results with different colors for each function
plt.figure(figsize=(10, 6))
colors = ['b', 'g', 'r', 'c', 'm', 'y']  # Define colors for each function
legend_labels = []  # Store legend labels for each function
for i, func_name in enumerate(stats.timings.keys()):
    timings = {}
    for entry in stats.timings[func_name]:
        lineno = entry[2]  # Line number is at index 2 of the tuple
        timing = entry[1]  # Total time is at index 1 of the tuple
        if lineno not in timings:
            timings[lineno] = timing
        else:
            timings[lineno] += timing
    sorted_timings = sorted(timings.items(), key=lambda x: x[0])
    line_numbers = [item[0] for item in sorted_timings]
    total_times = [item[1] for item in sorted_timings]
    plt.plot(line_numbers, total_times, marker='o', linestyle='-', color=colors[i])
    legend_labels.append(func_name)
plt.xlabel('Line Number')
plt.ylabel('Total Time (s)')
plt.title('Line-by-Line Profiling Results')
plt.grid(True)

# Add legend
plt.legend(legend_labels)

# Add profiling history in the corner
summary_str = lp.get_stats() #.get_stats().get_summary()
plt.figtext(0.1, 0.05, f'Profiling Summary:\n{summary_str}', fontsize=8, va="top")

# Show plot
plt.show()
