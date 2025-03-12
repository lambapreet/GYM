import random

def random_with_N_digits(n):
    """Generate a random number with exactly `n` digits."""
    if n <= 0:
        raise ValueError("Number of digits must be greater than 0")
    
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)
