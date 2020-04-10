#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    for index, weight in enumerate(weights):
        hash_table_insert(ht, weight, index)

    for i in range(0, limit):
        index1 = hash_table_retrieve(ht, i)
        if index1 is not None:
            # Remove index1 from hash table in case it's repeated
            hash_table_remove(ht, i)
            index2 = hash_table_retrieve(ht, limit - i)
            if index2 is not None:
                if index1 > index2:
                    return (index1, index2)
                return (index2, index1)

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
