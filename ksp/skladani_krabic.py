with open('skladani_krabic.txt', 'r', encoding='utf-8') as input_file:

    # read N
    N = int(input_file.readline().strip())

    # save lines to list
    box_sizes = [int(line.strip()) for line in input_file.readlines()]

# find the longest strictly increasing subsequence
lis = [1] * N
for i in range(N):
    for j in range(i):
        if box_sizes[j] < box_sizes[i]:
            lis[i] = max(lis[i], lis[j] + 1)

print(max(lis))
