from random import random
import datetime
alpha = 'Q5WE8RRT9RYU0TIOPLKJEHGFD0SAZX975CVBNM'


def RandomString():
    mystr = ''
    for i in range(1, 40):
        char = int(random() * len(alpha))
        mystr += alpha[char]
    return mystr
