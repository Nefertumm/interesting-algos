import numpy as np
import time as tm

def sieve_of_eratosthenes(n : int) -> list[int]:
    """ Find all prime numbers between 2 and a number n
    Intended to be O(n*log(log n))
    Source: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

    Args:
        n (int): top integer limit

    Returns:
        list: prime numbers between 2 and n
    """
    consecutive_numbers : list[bool] = [True for _ in range(n)]
    for i in range(2, int(np.sqrt(n) + 1)):
        if consecutive_numbers[i]:
            for j in range(i*i, n, i):
                consecutive_numbers[j] = False
    
    return [idx for idx, val in enumerate(consecutive_numbers) if val and idx >= 2]

n : int = int(input('N: '))
start : int = tm.perf_counter_ns()
primes : list[int] = sieve_of_eratosthenes(n)
end : int = tm.perf_counter_ns()
print(f"{primes} \nSize: {len(primes)} \nTime elapsed: {end - start}ns")
