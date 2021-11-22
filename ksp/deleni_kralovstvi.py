from queue import Queue

with open('deleni_kralovstvi.txt', 'r', encoding='utf-8') as input_file:

    # read number of towns
    n = int(input_file.readline().strip())

    # create adjacency list
    adj_list = [[] for _ in range(n)]

    # read roads and add to adjacency list
    for line in input_file.readlines():
        end_1, end_2 = tuple(int(x) for x in line.strip().split(' '))
        adj_list[end_1].append(end_2)
        adj_list[end_2].append(end_1)

# try coloring each town with a different color 1 or -1
color = [0] * n

# create queue for adjacent towns and a set of uncolored towns
queue = Queue()
uncolored = set(range(n))

division_possible = True

# continue until all towns are colored or some adjacent pair cannot be so
while uncolored and division_possible:

    # if queue is empty and there remain uncolored towns, add one to queue
    if queue.empty() and uncolored:
        first_uncolored = next(town for town in range(n) if not color[town])
        color[first_uncolored] = 1
        queue.put(first_uncolored)
        uncolored.remove(first_uncolored)

    # get a town from queue
    starting_town = queue.get()

    # color adjacent towns with different color
    for town in adj_list[starting_town]:
        if color[town] == color[starting_town]:
            # cannot be colored with different colors
            division_possible = False
            break

        if not color[town]:
            # if not colored yet, color and add to queue
            color[town] = -color[starting_town]
            queue.put(town)
            uncolored.remove(town)


if not division_possible:
    print('Nelze rozdělit.')
else:
    # otherwise the list of colors defines the division
    group_1 = (str(town) for town in range(n) if color[town] == 1)
    group_2 = (str(town) for town in range(n) if color[town] == -1)
    print(f'První skupina měst: {", ".join(group_1)}.')
    print(f'Druhá skupina měst: {", ".join(group_2)}.')
