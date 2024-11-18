import time
def timed_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Execute the function
        end_time = time.time()  # Record the end time
        
        print(f"{func.__name__} took {end_time - start_time:.6f} seconds to execute")
        return result  # Return the original function's result
    return wrapper