import hashlib
import ecdsa
import time
# An the previous block header - do not change any fields
previous_block_header = {
  "previousBlockHash": "651c16a0226d2ddd961c9391dc11f703c5972f05805c4fb45ab1469dda1d4b98",
  "payloadLength": 209,
  "totalAmountNQT": "383113873926",
  "generationSignature": "9737957703d4eb54efdff91e15343266123c5f15aaf033292c9903015af817f1",
  "generator": "11551286933940986965",
  "generatorPublicKey": "feb823bac150e799fbfc124564d4c1a72b920ec26ce11a07e3efda51ca9a425f",
  "baseTarget": 1229782938247303,
  "payloadHash": "06888a0c41b43ad79c4e4991e69372ad4ee34da10d6d26f30bc93ebdf7be5be0",
  "generatorRS": "NXT-MT4P-AHG4-A4NA-CCMM2",
  "nextBlock": "6910370859487179428",
  "requestProcessingTime": 0,
  "numberOfTransactions": 1,
  "blockSignature": "0d237dadff3024928ea4e5e33613413f73191f04b25bad6b028edb97711cbd08c525c374c3e2684ce149a9abb186b784437d01e2ad13046593e0e840fd184a60",
  "transactions": ["14074549945874501524"],
  "version": 3,
  "totalFeeNQT": "200000000",
  "previousBlock": "15937514651816172645",
  "cumulativeDifficulty": "52911101533010235",
  "block": "662053617327350744",
  "height": 2254868,
  "timestamp": 165541326
}
# you should edit the effective balance to be the last two digits from your user id
effective_balance = 67

def generate_ecdsa_key_pair():
    #generates a private key from a elliptic curve.
    signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    #generates a public key using above private key
    verifying_key = signing_key.get_verifying_key()
    return signing_key, verifying_key

def sign_message(message, signing_key):
    signature = signing_key.sign(message.encode())
    return signature

def compute_hit_value(signing_key):
    generation_signature = previous_block_header['generationSignature']
    # signs the previous generation signature with out signing key
    signature = sign_message(generation_signature, signing_key)
    print('Signature: ' + signature.hex())
    # hashes the result
    hash = hashlib.sha256(signature)
    print('Hash: ' + hash.hexdigest())
    # takes the first 8 bytes
    hit_value = hash.hexdigest()[:16]
    return hit_value

def time_to_find_new_block(hit_value):
    base_target = previous_block_header['baseTarget']
    start_time = time.time()
    time_elapsed = time.time() - start_time
    # finds the time at which the new target exceeds the hit value.
    while hit_value >= base_target * time_elapsed * effective_balance:
        time_elapsed = time.time() - start_time
    return time_elapsed

#gets ecdsa key pair
signing_key, verifying_key = generate_ecdsa_key_pair()
#signs Hello world using the private key
signature = sign_message('Hello world', signing_key)

print('Signing (Private) key: ' + signing_key.to_string().hex())
print('Verifying (Public) key: ' + verifying_key.to_string().hex())
print('Signature of Hello world: ' + signature.hex())
print('')
hit_value = compute_hit_value(signing_key)
print('Hit value: ' + hit_value)
time_elapsed = time_to_find_new_block(int(hit_value, 16))
print('Time taken: ' + str(time_elapsed))