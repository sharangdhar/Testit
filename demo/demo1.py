# true if n is prime
def isPrime(n):
  if n <= 1 or int(n) != n:
    return False
  for x in range(2, int(n*.5)+1):
    if n%x == 0:
      return False
  return True
