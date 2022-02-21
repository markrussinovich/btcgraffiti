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
UTXO_DEFAULT = 350

# implementation
from src.decode import decode_from_btc
from src.encode import encode_to_btc

#
# parse_commandline
# read arguments
#
def parse_commandline(descriptiontext):
    parser = argparse.ArgumentParser(prog='btcg-decode', 
        description=descriptiontext)
    parser.add_argument('transaction', metavar='transaction', help='Transaction to decode.')
    parser.add_argument('--net', "-n", default='main', choices=['main', 'test'], help='Either \'test\' or \'main\'' )
    args = parser.parse_args()    
    return args

#
# main
# Read file and encode it into a transaction
#
def main():
    sys.tracebacklimit=0
    descriptiontext='Read data from Bitcoin transaction.'
    print( '\nBTC Graffiti Decoder - by Mark Russinovich (@markrussinovich)')
    print( descriptiontext, '\n')
    args = parse_commandline( descriptiontext )

    # either encode or decode
    decode_from_btc( args.transaction, args.net )
    print('')

if __name__ == "__main__":
    main()