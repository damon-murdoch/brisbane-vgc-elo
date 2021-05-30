import math

# prob(a: int, b: int): int
# a: player 1 elo, b: player 2 elo
# Given the current elo ratings of two players, 
# calculate the probability of player 'a' beating player 'b'
def prob(a, b):

  # Calculate the probability of player 'a' beating player 'b'
  return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (a - b) / 400))

# rating(a: int, b: int, k: int, d: int): int
# a: player 1 elo, b: player 2 elo, 
# K: ranking modifier constant, d: winner (a = 0, b = 1)
def rating(a, b, K, d):

  # Probability of 'b' beating 'a'
  p_a = prob(b, a)

  # Probability of 'a' beating 'b'
  p_b = prob(a, b)

  if d: # If player 'b' wins:

    # a lost, reduce a's rating by
    # constant * 0 minus their probability of winning
    a = a + K * (0 - p_a)

    # b won, increase b's rating by
    # constant * 0 plus their probability of winning
    b = b + K * (1 - p_b)

  else: # If 'player 'a' wins

    # a won, increase a's rating by
    # constant * 0 plus their probability of winning
    a = a + K * (1 - p_a)

    # b lost, reduce b's rating by
    # constant * 0 minus their probability of winning
    b = b + K * (0 - p_b)

  return a, b

if __name__ == '__main__':

  a = 1000
  b = 1200
  K = 30
  d = 1

  print("Current Ratings: a:",a,"b:",b,'winner: b')
  print("K Constant:",K)

  # Update the rankings to the new values
  a, b = rating(a,b,K,d)

  print("Updated Ratings: a:",a,"b:",b)