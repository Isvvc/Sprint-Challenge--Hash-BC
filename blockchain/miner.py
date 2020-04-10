import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

def hash_digest(value):
    return hashlib.sha256(str(value).encode()).hexdigest()

def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last five digits of hash(p) are equal
    to the first five digits of hash(p')
    - IE:  last_hash: ...AE912345, new hash 12345888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()
    
    #last_proof_hash = hashlib.sha256(f"{last_proof}".encode()).hexdigest()
    last_proof_hash = hash_digest(last_proof)

    print("Searching for next proof")
    proof = random.randint(0, sys.maxsize)
    while not valid_proof(last_proof_hash, proof):
        proof = random.randint(0, sys.maxsize)

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    print(f"Last hash: {last_proof_hash}, proof hash: {hash_digest(proof)}")
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last five characters of
    the hash of the last proof match the first five characters of the hash
    of the new proof?

    IE:  last_hash: ...AE912345, new hash 12345E88...
    """

    #guess = f"{proof}".encode()
    #guess_hash = hashlib.sha256(guess).hexdigest()
    guess_hash = hash_digest(proof)
    return guess_hash[:5] == last_hash[-5:]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
