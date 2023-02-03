"""
encrypt_api_key
Copyright 2011 Brian Monkaba
Version 0.3 Revised by genBTC 2013
Version 0.323 Imported into other project 2023
"""
from Crypto.Cipher import AES
import hashlib
import json
import time
import random
import os
import getpass
import base64
import sys


def lock():
    print("\n\n*** genbtc.trader API Key Encryptor v0.323 - 2023 ***")
    print("-" * 30)
    print("\n\n")

    print("Enter the API KEY:")
    key = input().strip()

    print("\nEnter the API SECRET KEY:")
    secret = input().strip()

    print("\nEnter the site:")
    site = input().strip()

    print("\n\nEnter a new encryption password:")
    password = getpass.getpass().strip()  # uses raw_input() but doesnt keep a history

    print("\nGenerating the random salt.....")
    salt = os.urandom(32)  # requires Python 2.4  = 32 bytes or 256 bits of randomness
    fullpath = os.path.dirname(os.path.realpath(__file__))
    partialpath = os.path.join(fullpath + "/../keys/" + site)
    with open(os.path.join(partialpath + "_salt.txt"), "w") as f:
        f.write(salt)

    print("Generating the password hash.....\n")
    saltypass = password.encode("utf-8") + filesalt
    hash_pass = hashlib.sha512(saltypass).digest()
    crypt_key = hash_pass[:32]
    crypt_ini = hash_pass[-16:]  # create the AES container
    aes = AES.new(crypt_key, AES.MODE_OFB, crypt_ini)
    plaintext = json.dumps({"key": key, "secret": secret})

    # new way to pad. Uses 32 block length for the cipher 256 bit AES
    # chr(32) happens to be spacebar... (padding with spaces)
    pad = lambda s: s + (32 - len(s) % 32) * chr(32)  # function to pad the password
    paddedtext = pad(plaintext)

    ciphertext = aes.encrypt(paddedtext)  # go ahead and encrypt it
    print("Length after encryption =", len(ciphertext))

    print("Generating the encrypted API KEY file located in: %r" % (partialpath))
    with open(os.path.join(partialpath + "_key.txt"), "w") as f:
        print("Writing encryption key to file...")
        f.write(ciphertext)
        print("Done.")

    print("\n\nAttempting to re-verify just-written encrypted files...")
    with open(os.path.join(partialpath + "_key.txt"), "r") as f:
        filedata = f.read()
    with open(os.path.join(partialpath + "_salt.txt"), "r") as f:
        filesalt = f.read()

    loopcount=0
    retry = True
    while typo and loopcount<7:
        print("\nRe-enter your password again to confirm:")
        newpassword = getpass.getpass().strip()  # Just to check for typos
        if newpassword == password:
            retry = False
        else:
            failed("Incorrect password!!!!")
            loopcount+=1

    saltypass = password.encode("utf-8") + filesalt
    hash_pass = hashlib.sha512(saltypass).digest()
    crypt_key = hash_pass[:32]
    crypt_ini = hash_pass[-16:] # create the AES container
    decryptor = AES.new(crypt_key, AES.MODE_OFB, crypt_ini)

    def failed(message):
        os.remove(os.path.join(partialpath + "_key.txt"))
        os.remove(os.path.join(partialpath + "_salt.txt"))
        print("Failed verification due to %r. Please re-run again." % (message))

    print("File Read Verification Length = ", len(filedata))
    if len(filedata) % 16 == 0:
        try:
            filekeys = decryptor.decrypt(filedata)  # go ahead and decrypt the file
        except:
            failed("Failed AES Decryption")
        try:
            data = json.loads(filekeys)  # convert the string to a dict
        except:
            failed("Failed JSON Decoding")
        else:
            if data["key"] == key and data["secret"] == secret:
                print("\nPASSED Verification!!!!!!!!!!!!")
            else:
                failed("Failed API Key Verification")
    else:
        failed("Length was not 160. Make sure Length=160 or some multiple of 16.")


if __name__ == "__main__":
    lock()
