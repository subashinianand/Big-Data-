def partition(key, number_of_reducers):

    return hash(key) % number_of_reducers