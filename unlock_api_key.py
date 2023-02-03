#from my https://github.com/genbtc/trader.python/blob/master/lib/unlock_api_key.py
#
# unlock_api_key.py - from trader.python.genBTC-2013 + recoded/modified Feb 1 2023
# Description: quick gadget asks passwords and AES decrypts a file. (this is half 2/2)
# Usage: asks for a password to decrypt the file, or the pw can be param passed in
#        reads two files, site_salt.txt , site_key.txt
#        key.txt contains the real secrets, unlocked by a hashed and salted password
# Example Call-Site:
#  self._key, self._secret, self._passphrase = unlock_api_key.unlock("generic", encpassword)
from Crypto.Cipher import AES
import json
import getpass
import hashlib
import os

def unlock(site, enc_password="", retry=True):
    KEYDIR = os.path.join(os.path.realpath(__file__), "/../keys/")
    FILENAME = KEYDIR + site
    with open(os.path.join(FILENAME + "_salt.txt"), "r") as fsalt:
        salt = fsalt.read()
    loopcount = 0
    # loop to re-type password
    while retry:
        if loopcount > 7:
            return
        if enc_password == "":
            print("{}: Enter your API key file encryption password.".format(site))
            enc_password = getpass.getpass()  # raw_input()
            loopcount += 1
        try:
            # salt first, then hash the password
            saltedpass = enc_password.encode("utf-8") + salt
            hashedpass = hashlib.sha512(saltedpass).digest()
            # split message digest in two
            crypt_key = hashedpass[:32]  # first 32B is crypt key
            crypt_ini = hashedpass[-16:]  # last 16B is initialization vectors
            # _key.txt holds previously AES encrypted data.
            with open(os.path.join(FILENAME + "_key.txt"), "r") as fkey:
                ciphertext = fkey.read()
            # create an AES decryptor instance, hashedpass opens it
            decryptor = AES.new(crypt_key, AES.MODE_OFB, crypt_ini)
            plaintext = decryptor.decrypt(ciphertext)
            out = json.loads(plaintext)
            # return key , secret, and give password back too
            return (out["key"], out["secret"], enc_password)

        except Exception as e:
            print(
                """\n\n
                  Error: You _may_ have entered an Invalid Password!
                         Or, the encrypted api key File was File Not Found?
                  (note) P.S. IF you haven't yet generated the encrypted key file,
                              use the other encrypt_api_key.py script!! (half 1/2).
			             Something went wrong:\n"""  + e)
            enc_password = ""
