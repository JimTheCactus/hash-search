
# coding: utf-8

# # Project 1
# John-Michael O'Brien
# 01/24/2019
# 
# ## Part 1: Find a plaintext that hashes via SHA256 to a code that begins with >= 24 consecutive zeros
# We can constrain our search to only the first $2^{256}$ possible messages (i.e. messages 256 bits long.) The reason for this is that we know via the pidgeon hole principle that longer messages are extremely likely to collide with these first $2^{256}$ messages so long as the hash algorithm produces a minimum of collssions. This simplifies our search. If we also presume that SHA256 does not have any significant non-uniformity in its density, then what numbers we check don't matter; the chances of finding what we're looking for are the same. As such, to maximize the search speed; I'm simply starting from a number $n_0$ and counting up.

# In[7]:


# Pull in the hash tools
import os
import secrets
import hashlib
import redis


# Server to connect to.
server = os.getenv('REDIS_SERVER','redis1')

# Connect to the server
r = redis.StrictRedis(host=server, port=6379, db=0)


# Set the intial number for the search
initial_n = secrets.randbits(255)

# Start in the upper half
initial_n |= 1<<255

# Precalculate the byte array for the mandetory header
prefix = "joob7131-made0661-".encode("utf-8")

# Initialize our best run variables
longest_hash = []
longest_text = []
longest_run = 0

n = initial_n


# In[ ]:


print("Initial n: ", n)

# Loop until we find a run with 24 or more bits.
while True:
    # Build up the message by prepending the prefix
    msg = prefix + str(n).encode('utf-8')
    # And calculate the hash
    result = hashlib.sha256(msg).digest()
    
    # Starting from position 0
    j=0
    
    # Check each byte until we find a non-zero byte
    while result[j] == 0:
        j+=1

    # Work out how many bits that is
    bits = j*8
    
    # Grab the first non-zero byte
    last_byte = result[j]
    
    # And shift it left until we find the first non-zero bit
    while last_byte & 0x80 == 0:
        last_byte <<= 1
        bits+=1
    
    # If it's the longest run we've seen so far
    if bits > longest_run:
        # Set it aside
        longest_hash = result
        longest_run = bits
        longest_text = msg
        posted = r.setnx(
            "hash-search/{0}".format(longest_run).encode("utf-8"),
            "{0} {1}".format(longest_text.decode('utf-8'),longest_hash.hex()).encode("utf-8")
            )
        print(
            "Total bits:", bits,
            "hash:", longest_hash.hex(),
            "msg:", "'" + longest_text.decode('utf-8') + "'",
            "posted:", posted,
            flush=True
            )
        f = open("preimage-longest.txt", "w")
        f.write(longest_text.decode('utf-8') + " " + longest_hash.hex())
        f.write("\n")
        f.close()

    # And try the next number
    n+=1

