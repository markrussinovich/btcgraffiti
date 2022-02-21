# BTC-Graffiti

BTC-Graffitti is a pair of scripts where btcg-encode encode a specified file into a Bitcoin transaction using the Pay-2-Fake-Hash (P2FS) technique that encodes data 
into transaction output script addresses, and btcg-decode extracts the addresses and reconsistitutes the encoded file. The encoder stores the name of the source file 
in the OP_RETURN and the decode script stores the extracted data to that file name. The data it encodes can be of any format, 
including text, images, or audio. Content you store this way is **permanent**. Because data BTC-Graffiti lives forever on the Bitcoin blockchain,  BTCG-Graffiti posts make
the pefect birtdhay or Valentine's day gift. 

## Encoding Data
To encode a file, invoke the encoding script like this:

    > python btcg-encode.py <file> --key KEY [--utxo UTXO] [--net <main|test>]

The private key corresponds to the account that holds the Bitcoin the script uses for the transaction and must be in WIF compressed format. An easy way to generate an 
an address/key pair compatible with the script is to use [bitaddress.org](http://bitaddress.org) and send data from an existing address to that one for use by the script. 

## Decoding Data
To decode a transaction that has BTC-Graffiti data encoded into it, use the decoding script like this:

    python btcg-decode <transaction> [--net <main|test>]
    
This example downloads a test message BTC-Graffiti stored in a transaction: 

    > python btcg-decode.py bd71fc8ceadc75a35f0c96556aabcc24a24bc458e4167969ed62ec7fe1efd024
    
    BTC Graffiti Decoder - by Mark Russinovich (@markrussinovich)
    Read data from  Bitcoin transaction.

    Reading transaction...
    Writing encoded data to test.txt...
    Transaction decoded to test.txt.
    
    > type test.txt
    BTGC lives forever!
    
And this transaction is a tribute to Satoshi, storing the abstract for his paper announcing Bitcoin: 

    > python btcg-decode.py c8a7afbff7d11b3627bb43251843394dfbf26d696e0f475950ac2fd39d5b4c2b

    BTC Graffiti Decoder - by Mark Russinovich (@markrussinovich)
    Read data from  Bitcoin transaction.

    Reading transaction...
    Writing encoded data to satoshi.png...
    Transaction decoded to satoshi.png.

This is the image saved to satoshi.png:

![Satoshi.png](/Satoshi.png "Satoshi.png")
