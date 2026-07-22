def split_input(filename, chunk_size):

    with open(filename, "r") as file:
        lines = file.readlines()

    chunks = []

    for i in range(0, len(lines), chunk_size):

        chunks.append(lines[i:i + chunk_size])

    return chunks