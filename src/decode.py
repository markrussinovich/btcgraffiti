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
# decode_file
# decode the transaction outputs into a file
#
def decode_file( txouts, file ):
    filebytes = []

    # ignore last txout which is the miner fee
    for i in range(len(txouts)-1):
        filebytes += bytes(decode_txout(txouts[i]))
    filelen = decode_int(BytesIO(bytes(filebytes[0:])), 4)

    if len(filebytes)-4 > filelen + HASH_SIZE or len(filebytes)-4 < filelen - HASH_SIZE:
        print('Error: Unrecognized encoding.')
        quit()
    try:
        f = open(file, 'wb')
        f.write( bytes(filebytes[4:4+filelen]))
    except IOError as e:
        print('Error writing ', file, ': ', e )
        raise
    

#
# decode_from_btc
# decode a transaction to extract media content
#
def decode_from_btc( tx, net, file ):
    print( 'Reading transaction...')
    if net == 'main':
        txbytestring = NetworkAPI.get_transaction_by_id( tx )
    else:
        txbytestring = NetworkAPI.get_transaction_by_id_testnet( tx )
    txbytes = bytes.fromhex(txbytestring)
    tx = Tx.decode(BytesIO(txbytes))

    print( 'Writing encoded data to file...')
    decode_file( tx.tx_outs, file )
    print('Transaction decoded to ', file)
