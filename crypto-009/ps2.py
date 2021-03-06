#!/usr/bin/env python

import binascii
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from Crypto.Util import Counter


# Example usage of Python Crypto library.
# http://www.inconteam.com/software-development/41-encryption/55-aes-test-vectors

# CBC
key = '2b7e151628aed2a6abf7158809cf4f3c'
iv = '000102030405060708090A0B0C0D0E0F'
message = '6bc1bee22e409f96e93d7e117393172a'
ciphertext = '7649abac8119b246cee98e9b12e9197d'

obj = AES.new(unhexlify(key), AES.MODE_CBC, unhexlify(iv))
c = obj.encrypt(unhexlify(message))
assert hexlify(c) == ciphertext

obj = AES.new(unhexlify(key), AES.MODE_CBC, unhexlify(iv))
m = obj.decrypt(unhexlify(ciphertext))
assert hexlify(m) == message

# CTR
key = '2b7e151628aed2a6abf7158809cf4f3c'
iv = 'f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'
message = '6bc1bee22e409f96e93d7e117393172a'
ciphertext = '874d6191b620e3261bef6864990db6ce'

ctr = Counter.new(128, initial_value=int(iv, 16))
obj = AES.new(unhexlify(key), AES.MODE_CTR, unhexlify(iv), counter=ctr)
c = obj.encrypt(unhexlify(message))
assert hexlify(c) == ciphertext

ctr = Counter.new(128, initial_value=int(iv, 16))
obj = AES.new(unhexlify(key), AES.MODE_CTR, unhexlify(iv), counter=ctr)
m = obj.decrypt(unhexlify(ciphertext))
assert hexlify(m) == message


# Question 1
# CBC
key1 = '140b41b22a29beb4061bda66b6747e14'
ciphertext1 = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'
iv1 = ciphertext1[0:32]
ciphertext1 = ciphertext1[32:]

# Question 2
# CBC
key2 = '140b41b22a29beb4061bda66b6747e14'
ciphertext2 = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'
iv2 = ciphertext2[0:32]
ciphertext2 = ciphertext2[32:]

# Question 3
# CTR
key3 = '36f18357be4dbd77f050515c73fcf9f2'
ciphertext3 = '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'
iv3 = ciphertext3[0:32]
ciphertext3 = ciphertext3[32:]

# Question 4
key4 = '36f18357be4dbd77f050515c73fcf9f2'
ciphertext4 = '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'
iv4 = ciphertext4[0:32]
ciphertext4 = ciphertext4[32:]


# http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
def pkcs5_unpad(s):
    s = s[0:-ord(s[-1])]
    return s


def pkcs5_pad(s):
    BLOCK_SIZE = 16
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

print 'PyCrypto'

# Decryption
obj1 = AES.new(unhexlify(key1), AES.MODE_CBC, unhexlify(iv1))
message1 = obj1.decrypt(unhexlify(ciphertext1))
foo1 = message1
assert pkcs5_pad(pkcs5_unpad(message1)) == message1
message1 = pkcs5_unpad(message1)
print 'Message 1:', message1
assert message1 == 'Basic CBC mode encryption needs padding.'

obj2 = AES.new(unhexlify(key2), AES.MODE_CBC, unhexlify(iv2))
message2 = obj2.decrypt(unhexlify(ciphertext2))
message2 = pkcs5_unpad(message2)
print 'Message 2:', message2
assert message2 == 'Our implementation uses rand. IV'

ctr3 = Counter.new(128, initial_value=int(iv3, 16))
obj3 = AES.new(unhexlify(key3), AES.MODE_CTR, unhexlify(iv3), counter=ctr3)
message3 = obj3.decrypt(unhexlify(ciphertext3))
print 'Message 3:', message3

ctr4 = Counter.new(128, initial_value=int(iv4, 16))
obj4 = AES.new(unhexlify(key4), AES.MODE_CTR, unhexlify(iv4), counter=ctr4)
message4 = obj4.decrypt(unhexlify(ciphertext4))
print "Message 4:", message4

# Encryption
obj1 = AES.new(unhexlify(key1), AES.MODE_CBC, unhexlify(iv1))
message1 = pkcs5_pad(message1)
c1 = obj1.encrypt(message1)
assert hexlify(c1) == ciphertext1

obj2 = AES.new(unhexlify(key2), AES.MODE_CBC, unhexlify(iv2))
message2 = pkcs5_pad(message2)
c2 = obj2.encrypt(message2)
assert hexlify(c2) == ciphertext2

ctr3 = Counter.new(128, initial_value=int(iv3, 16))
obj3 = AES.new(unhexlify(key3), AES.MODE_CTR, unhexlify(iv3), counter=ctr3)
c3 = obj3.encrypt(message3)
assert hexlify(c3) == ciphertext3

ctr4 = Counter.new(128, initial_value=int(iv4, 16))
obj4 = AES.new(unhexlify(key4), AES.MODE_CTR, unhexlify(iv4), counter=ctr4)
c4 = obj4.encrypt(message4)
assert hexlify(c4) == ciphertext4


def aes_cbc_decrypt(key, iv, ciphertext):
    key_length = len(key)
    ciphertext_length = len(ciphertext)
    iv_length = len(iv)
    block_size = 16  # 128 bits

    assert key_length == 16
    assert ciphertext_length % block_size == 0

    num_blocks = ciphertext_length / block_size
    message = ''

    for i in range(num_blocks):
        c = ciphertext[(i * block_size):((i + 1) * block_size)]
        k = key
        obj = AES.new(k, AES.MODE_CBC, iv)
        m = obj.decrypt(c)
        message += m
        iv = c

    return message


def aes_cbc_encrypt(key, iv, message):
    ciphertext = ''
    return


print 'Own implementation'

message = aes_cbc_decrypt(unhexlify(key1), unhexlify(iv1), unhexlify(ciphertext1))
print message

message = aes_cbc_decrypt(unhexlify(key2), unhexlify(iv2), unhexlify(ciphertext2))
print message

message = 'Basic CBC mode encryption needs padding.'
#print len(message)
#ciphertext = aes_cbc_encrypt(unhexlify(key1), unhexlify(iv1), unhexlify(m1))
