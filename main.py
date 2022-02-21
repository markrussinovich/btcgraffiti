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
from utils.keys import *
from utils.ecdsa import *
from bit import network
from bit import Key, wif_to_key, PrivateKey, PrivateKeyTestnet
import argparse
from io import BytesIO

# Approximate amount of utxo that mainnet seems to accept
UTXO_DEFAULT = 200

# implementation
from src.decode import decode_from_btc
from src.encode import encode_to_btc

#
# parse_commandline
# read arguments
#
def parse_commandline(descriptiontext):
    parser = argparse.ArgumentParser(prog='btcgraffiti', 
        description=descriptiontext)
    parser.add_argument('fileortransaction', metavar='<file|transaction>', help='name of file to post or to decode into')
    parser.add_argument('--key', "-k", help='Account key. Required for encoding data' )
    parser.add_argument('--net', "-n", default='main', choices=['main', 'test'], help='Either \'test\' or \'main\'' )
    parser.add_argument('--utxo', '-u', help='Amount of Satoshi UTXO to waste on each encoded output. Mainnet can reject small amounts, or \'dust\'')
    args = parser.parse_args()    
    return args

#
# main
# Read file and encode it into a transaction
#
def main():
    sys.tracebacklimit=0
    descriptiontext='Write data into Bitcoin transactions and read data from them.'
    print( '\nBTC Graffiti - by Mark Russinovich (@markrussinovich)')
    print( descriptiontext, '\n')
    args = parse_commandline( descriptiontext )

    # either encode or decode
    if args.key != None:
        if args.utxo == None:
            if args.net == 'test':
                args.utxo = 1
            else:
                args.utxo = UTXO_DEFAULT
        encode_to_btc( args.key, args.net, args.fileortransaction, args.utxo )
    else:
        decode_from_btc( args.fileortransaction, args.net )
    print('')

if __name__ == "__main__":
    main()