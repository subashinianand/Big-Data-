def mapper(line):

    words = line.strip().split()

    output = []

    for word in words:
        output.append((word, 1))

    return output