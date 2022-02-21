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
from src.encode import HASH_SIZE
from utils.transaction import *
from utils.keys import *
from utils.ecdsa import *
from bit import network
from bit.network import NetworkAPI
from bit import Key, wif_to_key, PrivateKey, PrivateKeyTestnet
from io import BytesIO

#
# decode_txout
# validate transaction output
#
def decode_txout( txout: TxOut ):
    # make sure it's a standard Pk2H
    cmds = txout.script_pubkey.cmds
    if len(cmds) != 5:
        return None
    if isinstance(cmds[0], int) and (OP_CODE_NAMES[cmds[0]] == 'OP_DUP') != True: 
        return None
    if isinstance(cmds[1], int) and (OP_CODE_NAMES[cmds[1]] == 'OP_HASH160') != True: 
        return None
    if isinstance(cmds[2], bytes) != True: # hash
        return None
    if isinstance(cmds[3], int) and (OP_CODE_NAMES[cmds[3]] == 'OP_EQUALVERIFY') != True: 
        return None
    if isinstance(cmds[4], int) and (OP_CODE_NAMES[cmds[4]] == 'OP_CHECKSIG')!= True: 
        return None
    return txout.script_pubkey.cmds[2]

#
# verify_btcgmarker
#
def verify_btcgmarker( txouts ):
    for i in range(len(txouts)):
        cmds = txouts[i].script_pubkey.cmds
        if len(cmds) == 2 and isinstance(cmds[0], int) and OP_CODE_NAMES[cmds[0]] == 'OP_RETURN':
            return txouts[i].script_pubkey.cmds[1]
    return None

#
# decode_file
# decode the transaction outputs into a file.
# returns the OP_RETURN message
#
def decode_file( txouts ):
    filebytes = []

    # make sure this is one of ours by looking for marker in OP_RETURN
    btcgmarker = verify_btcgmarker( txouts ) 
    if btcgmarker == None:
        print( 'Error: Not a BTC Graffiti transaction.')   
        quit()
    filename = str(btcgmarker[5:], 'utf-8')
    print( 'Writing encoded data to {}...'.format(filename))

    # ignore last two txouts: last one is the OP_RETURN message
    # and second to last is remainding unspent
    for i in range(len(txouts)-2):
        filebytes += bytes(decode_txout(txouts[i]))
    filelen = decode_int(BytesIO(bytes(filebytes[0:])), 4)

    if len(filebytes)-4 > filelen + HASH_SIZE or len(filebytes)-4 < filelen - HASH_SIZE:
        print('Error: Unrecognized encoding.')
        quit()
    try:
        f = open(filename, 'wb')
        f.write( bytes(filebytes[4:4+filelen]))
        f.close()
    except IOError as e:
        print('Error writing {}:'.format(filename))
        print(  e )
        raise
    return filename
    

#
# decode_from_btc
# decode a transaction to extract media content
#
def decode_from_btc( tx, net ):
    print( 'Reading transaction...')
    if net == 'main':
        txbytestring = NetworkAPI.get_transaction_by_id( tx )
    else:
        txbytestring = NetworkAPI.get_transaction_by_id_testnet( tx )
    txbytes = bytes.fromhex(txbytestring)
    tx = Tx.decode(BytesIO(txbytes))

    # writ to file
    filename = decode_file( tx.tx_outs )
    print('Transaction decoded to {}.'.format(str(filename)))
