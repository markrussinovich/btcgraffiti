
from email.mime import image
import sys
from utils.transaction import *
from utils.keys import *
from utils.ecdsa import *
from bit import network
from bit import Key, wif_to_key, PrivateKey, PrivateKeyTestnet
import argparse
from io import BytesIO

# implementation
from src.decode import decode_from_btc
from src.encode import encode_to_btc


#
# parse_commandline
# read arguments
#
def parse_commandline():
    parser = argparse.ArgumentParser(description='A script that encodes the specified image and posts a transaction to the Bitcoin blockchain')
    parser.add_argument(prog='btcgraffiti')
    parser.add_argument('file', metavar='file', help='name of file to post or to decode into')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--key', "-k", help='Account key' )
    group.add_argument('--transaction', "-tx", help='Transaction to decode' )
    parser.add_argument('--net', "-n", default='main', choices=['main', 'test'], help='Either \'test\' or \'main\'' )
    args = parser.parse_args()    
    return args

#
# main
# Read file and encode it into a transaction
#
def main():
    sys.tracebacklimit=0
    args = parse_commandline()

    # either encode or decode
    print(args.prog)
    if args.key != None:
        encode_to_btc( args.key, args.net, args.file )
    else:
        decode_from_btc( args.transaction, args.net, args.file )


if __name__ == "__main__":
    main()