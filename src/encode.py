#
# BTC Graffiti
# by Mark Russinovich
#
# Copyright (c) 2022 by Mark Russinovich
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
from email.mime import image
import sys
from utils.transaction import *
from utils.keys import b58encode, address_to_pkb_hash
from bit import network
from bit import Key, PrivateKey, PrivateKeyTestnet
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
def encode_file( filebytes, net, utxo ):
    txouts = []
    filelen = len(filebytes)

    filestream =  filelen.to_bytes(4,'little')
    filestream = filestream + filebytes
    filestreamlen = len(filestream)
    for block in range(int((filestreamlen+HASH_SIZE-1)/HASH_SIZE)):
        blockbytes = filestream[block*HASH_SIZE:min(filestreamlen, block*HASH_SIZE+HASH_SIZE)]
        blockbytes = blockbytes + bytes( HASH_SIZE-len(blockbytes))
        txout = (base58encode(blockbytes, net ), utxo, 'satoshi')
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
        print('Error reading {}:'.format(file ))
        print( e )
        raise
    if len(binarycontent) == 0:
        raise("File is zero length")
    return binarycontent

#
# encode_to_btc
# Encode a file into a bitcoin transaction and post it
#
def encode_to_btc( key, net, file, utxo ):
    # read the input file
    print('Encoding \'{}\'...'.format( file))
    filebytes = read_file( file )

    # encode image in outputs 
    txouts = encode_file( filebytes, net, utxo )   

    # get key
    if net == 'test':
        key = PrivateKeyTestnet( key ) 
    else:
        key = PrivateKey( key )
    print('Looking up account balance for {}...'.format( key.address ))
    balance =  float(key.get_balance('satoshi'))
    
    # fire off the transaction!
    try: 
        # save marker and file name in OP_RETURN
        filepath = os.path.split(file)
        btcgmessage='BTGC:'+filepath[1] 
        txid = key.send( txouts, message=btcgmessage )
    except Exception as inst:
        print( 'Error posting transaction:')
        print( inst )
        return 
    
    print('File encoded to transaction', txid )
    return 