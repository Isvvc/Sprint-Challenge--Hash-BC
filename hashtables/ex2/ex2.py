#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * (length - 1)

    next_destination = None

    for ticket in tickets:
        if ticket.source == "NONE":
            route[0] = ticket.destination
            next_destination = ticket.destination
        else:
            hash_table_insert(hashtable, ticket.source, ticket.destination)

    for i in range(1, length - 1):
        destination = hash_table_retrieve(hashtable, next_destination)
        route[i] = destination
        next_destination = destination

    return route
