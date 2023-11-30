import random
def random_camelot():
    numbers = list(range(1, 13))
    letters = ['A', 'B']
    return [(random.choice(numbers), random.choice(letters)) for _ in range(50)]
