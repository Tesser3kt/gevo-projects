x = int(input('Zadej mocninu dvojky: '))

count = 0
while x % 2 == 0:
    x = x // 2
    count = count + 1

print(count)
print(2 ** count)
list = [2, 4, 5, 6]
vytisknete 4, 8, 10, 12 (kazdy cislo x dva)
