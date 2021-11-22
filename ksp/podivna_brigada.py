with open('podivna_brigada.txt', 'r', encoding='utf-8') as input_file:

    # read N, not like it helps anything...
    N = int(input_file.readline().strip())

    # init working time counters and read lines
    kevin, sarah = 0, 0
    for line in input_file.readlines():
        processing_time = int(line.strip())

        # the document goes to the one with lower working time
        if kevin <= sarah:
            kevin += processing_time
        else:
            sarah += processing_time

print(max(kevin, sarah))
