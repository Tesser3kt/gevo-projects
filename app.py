from random import randint


x = [[randint(1, 9) for _ in range(5)] for _ in range(5)]

for i in range(5):
    print(x[i][i])
