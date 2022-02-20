from email.mime import image
import sys
from utils.transaction import *
from utils.keys import *
from utils.ecdsa import *
from bit import network
from bit import Key, wif_to_key, PrivateKey, PrivateKeyTestnet
import argparse
from io import BytesIO

# Size of a public key hash in bytes (160 bits)
HASH_SIZE = 20

#
# base58encode
# take public key and encode it into a BTC address
#
def base58encode( pkb_hash, net ):
    if net == 'main':
        ver_pkb_hash = b'\x00' + pkb_hash
    else:
        ver_pkb_hash = b'\x6f' + pkb_hash

    # calculate the checksum
    checksum = sha256(sha256(ver_pkb_hash))[:4]
    # append to form the full 25-byte binary Bitcoin Address
    byte_address = ver_pkb_hash + checksum

    # finally b58 encode the result
    b58check_address = b58encode(byte_address)
    return b58check_address



#
# encode_file
# take an image byte stream, add a length to the front
# and encode it into a tx output
#
def encode_file( filebytes, net ):
    txouts = []
    filelen = len(filebytes)

    filestream =  filelen.to_bytes(4,'little')
    filestream = filestream + filebytes
    filestreamlen = len(filestream)
    for block in range(int((filestreamlen+HASH_SIZE-1)/HASH_SIZE)):
        blockbytes = filestream[block*HASH_SIZE:min(filestreamlen, block*HASH_SIZE+HASH_SIZE)]
        blockbytes = blockbytes + bytes( HASH_SIZE-len(blockbytes))
        #print( block, '(', len(blockbytes), ')', ': ', blockbytes )
    
        txout = (base58encode(blockbytes, net ), 1, 'satoshi')
        txouts.append(txout)
    
    return txouts


#
# read_file
# read an file bytestream
#
def read_file( file ):
    try:
        f = open(file, 'rb')
        binarycontent = f.read(-1)  
    except IOError as e:
        print('Error reading ', file, ': ', e )
        raise
    if len(binarycontent) == 0:
        raise("File is zero length")
    return binarycontent

#
# encode_to_btc
# Encode a file into a bitcoin transaction and post it
#
def encode_to_btc( key, net, file ):
    # read the input file
    print('Encoding \'', file, '\'...')
    filebytes = read_file( file )

    # encode image in outputs 
    txouts = encode_file( filebytes, net )   

    # get key
    if net == 'test':
        key = PrivateKeyTestnet( key ) 
    else:
        key = PrivateKey( key )
    print('Looking up account balance for ', key.address, '...' )
    if( float(key.get_balance('btc')) < 0.0001 ):
        print( 'Not enough funds in account', key.address, ' for transaction:\n')
    
    # fire off the transaction!
    try: 
        txid = key.send( txouts )
    except Exception as inst:
        print( inst )
        return 
    
    print('File encoded to transaction ', txid )
    return 