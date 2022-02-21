# BTC-Graffiti

BTC-Graffitti is a pair of scripts where btcg-encode encode a specified file into a Bitcoin transaction using the Pay-2-Fake-Hash (P2FS) technique that encodes data 
into transaction output script addresses, and btcg-decode extracts the addresses and reconsistitutes the encoded file. The encoder stores the name of the source file 
in the OP_RETURN and the decode script stores the extracted data to that file name. The data it encodes can be of any format, 
including text, images, or audio. Content you store this way is **permanent**. Because data BTC-Graffiti posts lives forever on the Bitcoin blockchain,  BTC-Graffiti posts make
the pefect birtdhay or Valentine's day gift. 

## Encoding Data
To encode a file, invoke the encoding script like this:

    > python btcg-encode.py <file> --key KEY [--utxo UTXO] [--net <main|test>]

The private key corresponds to the account that holds the Bitcoin the script uses for the transaction and must be in WIF compressed format. An easy way to generate an 
an address/key pair compatible with the script is to use [bitaddress.org](http://bitaddress.org) and send data from an existing address to that one for use by the script. 

Here's an example command that successfully encoded data:

    > python btcg-encode.py satoshi.png --key #########
    
    BTC Graffiti Encoder - by Mark Russinovich (@markrussinovich)
    Write data into Bitcoin transactions.

    Encoding 'satoshi.png'...
    Looking up account balance for 1Lc35WwyqSbW4quqY8CNHrVmjUXsK2Xcwq...
    File encoded to transaction c8a7afbff7d11b3627bb43251843394dfbf26d696e0f475950ac2fd39d5b4c2b


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
    BTCG lives forever!
    
And this transaction is a tribute to Satoshi, storing the abstract for his paper announcing Bitcoin: 

    > python btcg-decode.py c8a7afbff7d11b3627bb43251843394dfbf26d696e0f475950ac2fd39d5b4c2b

    BTC Graffiti Decoder - by Mark Russinovich (@markrussinovich)
    Read data from  Bitcoin transaction.

    Reading transaction...
    Writing encoded data to satoshi.png...
    Transaction decoded to satoshi.png.

This is the image saved to satoshi.png:

![Satoshi.png](/Satoshi.png "Satoshi.png")

## Implementation

BTC-Graffiti uses the Bit Python library for creating and transmitting transactions, and functions from the Cryptos python library for decoding them: 

- [Bit Python Library](https://ofek.dev/bit/guide/intro.html)
- [Cryptos Library](https://github.com/karpathy/cryptos)

## Data on the Bitcoin Blockchain

People have been storing data on the Bitcoin blockchain, starting with Satoshi's genesis block message. Here are some sites and papers that discuss encoding techniques, 
the implications of data immutability, and give examples of other data encoded on Bitcoin:

 - [Data insertion in Bitcoin's Blockchain](https://digitalcommons.augustana.edu/cgi/viewcontent.cgi?article=1000&context=cscfaculty) This paper describes different techniques for encoding data into Bitcoin transactions. BTC-Graffiti uses the most straightforward technique, albiet one of the more inefficient ones. 
 - [A Quantitative Analysis of the Impact of Arbitrary Blockchain Content on Bitcoin](https://fc18.ifca.ai/preproceedings/6.pdf) A paper from 2018 that explores the benefits and risks of Bitcoin's support for storing arbitrary data. 
 - [Bitcoin's Greatest Feature Is Also Its Existenital Threat](https://www.schneier.com/essays/archives/2021/03/bitcoins-greatest-feature-is-also-its-existential-threat.html) Bruce Schneier's post explores the implications of Bitcoin's blockchain containing objectionable, or even illegal, content. 
- [Hidden surprises in the Bitcoin blockchain and how they are stored: Nelson Mandela, Wikileaks, photos, and Python software](http://www.righto.com/2014/02/ascii-bernanke-wikileaks-photographs.html) This post points at Bitcoin transactions that have encoded data. 
- [Edit transactions for blockchains](https://patents.google.com/patent/US10592873B2/en) A design I came up with that would enable a blockahin network like Bitcoin to edit out content while preserving the integrity of the ledger. This wouldn't prevent the data from continuing on in forks and archives, but it would remove it from the fork that agrees to the removal. 
