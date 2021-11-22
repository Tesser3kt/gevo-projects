with open('dynova_polevka.txt', 'r', encoding='utf-8') as input_file:
    # read first line
    D, S, N = tuple(int(x)
                    for x in input_file.readline().strip().split(' '))

    # read shops and count stops
    stops = 0
    for line in input_file.readlines():

        # read opening hours
        A, B = tuple(int(x) for x in line.strip().split(' '))

        # if counter is within opening hours, add 10 seconds and a stop
        if A <= S <= B:
            S += 10
            stops += 1

        # move to another shop
        S += D

print(stops)
