import hashlib
import json
import time

# An example block header - do not change any fields except nonce and coinbase_addr
example_block_header = {'height': 1478503,
                        'prev_block': '0000000000000da6cff8a34298ddb42e80204669367b781c87c88cf00787fcf6',
                        'total': 38982714093,
                        'fees': 36351,
                        'size': 484,
                        'ver': 536870912,
                        'time': 1550603039.882228,
                        'bits': 437239872,
                        'nonce': 0,                     #You may change this field of the block
                        'coinbase_addr': 'bzqs27',     #You should change this field of the block to your studentID
                        'n_tx': 2,
                        'mrkl_root': '69224771b7a2ed554b28857ed85a94b088dc3d89b53c2127bfc5c16ff49da229',
                        'txids': ['3f9dfc50198cf9c2b0328cd1452513e3953693708417440cd921ae18616f0bfc', '3352ead356030b335af000ed4e9030d487bf943089fc0912635f2bb020261e7f'],
                        'depth': 0}

def double_hash():
    # Simplified conversion of block header into bytes:
    block_serialised = json.dumps(example_block_header, sort_keys=True).encode()
    # Double SHA256 hashing of the serialised block
    block_hash=hashlib.sha256(hashlib.sha256(block_serialised).digest()).hexdigest()
    return block_hash
    
def compute_target(difficulty):
    #sets initial target for difficulty 1
    initial_target_int = int('00000000FFFF0000000000000000000000000000000000000000000000000000', 16)
    #calculates current target
    current_target_int = int(initial_target_int / difficulty)
    return current_target_int

def find_nonce(block_hash, target_int):
    block_hash_int = int(block_hash, 16)
    # terminates when we find a hash larger than out target value.
    while target_int < block_hash_int :
        #increments the nonce
        example_block_header['nonce'] += 1
        #hashes the resulting header
        new_hash = double_hash()
        block_hash_int = int(new_hash, 16)

    return example_block_header['nonce']
start = time.time()
block_hash = double_hash()
target_int = compute_target(0.001)
nonce = find_nonce(block_hash, target_int)
# total time to find a nonce.
print('Time elapsed: '+ str(time.time() - start))
print('Target hash: ' + str(hex(target_int)))
print('Valid hash with nonce ' + str(example_block_header['nonce'])+': '+block_hash)
