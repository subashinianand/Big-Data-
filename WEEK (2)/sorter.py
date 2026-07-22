def sort_partition(filename):

    with open(filename, "r") as file:

        data = []

        for line in file:

            key, value = line.split()

            data.append((key, int(value)))

    # Sort by key
    data.sort(key=lambda x: x[0])

    with open(filename, "w") as file:

        for key, value in data:

            file.write(f"{key} {value}\n")