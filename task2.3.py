import blockcypher

def generate_address(token):
    #this is the code provided in the assignment, we don't use it as we already have an address.
    address_object = blockcypher.generate_new_address(coin_symbol='btc-testnet', api_key=token)
    address = address_object['address']
    private_keys=[address_object['private']]
    public_keys=[address_object['public']]
    return  address, private_keys, public_keys

def sign_transaction(transaction, public_keys, private_keys):
    #makes a transaction signature using our transaction, and keys.
    signatures = blockcypher.make_tx_signatures(txs_to_sign=transaction['tosign'], privkey_list=private_keys, pubkey_list=public_keys)
    #broadcasts the signed transaction
    blockcypher.broadcast_signed_transaction(unsigned_tx=transaction, signatures=signatures, pubkeys=public_keys, coin_symbol='btc-testnet', api_key='471c0c64d43d49528b729ea543b201c1')

def make_transaction_proof_of_burn(token, address):
    #specifies input address
    inputs = [{'address': address}]
    #gets hex-encoding of user ID.
    user_id_hex = 'bzqs27'.encode().hex()
    #concatenates the user ID encoding to the OP codes for OP_RETURN OP_PUSHDATA1 and the number of bytes 06
    message = '6a4c06' + user_id_hex
    #adds this script to the output.
    outputs = [{'value': 0, 'script_type':"null-data", 'script': message}]
    # creates the transaction shell
    transaction = blockcypher.create_unsigned_tx(inputs=inputs, outputs=outputs, coin_symbol='btc-testnet', api_key=token)
    return transaction

token = '471c0c64d43d49528b729ea543b201c1'
#address, private_keys, public_keys = generate_address(token)

#the below addresses and private/public keys were generated by our generate address function, for the token stated above.
address = 'mqCYbVBd7jYKtGLoJMbfwWyi1PFFrxuVGA'
private_keys = ['270c3c84c28d315c8ccb1da24d38ed4bca54e1c811614cd093978ae30782bc12']
public_keys = ['0242798c31a4745fb1e83970866fce29071a87f3a92e329a47c0e5116831bf74ad']

#makes the transaction
transaction = make_transaction_proof_of_burn(token, address)
#signs the transaction
sign_transaction(transaction, public_keys, private_keys)
print('Transaction complete.')