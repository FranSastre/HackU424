import base64
import binascii
from Crypto.Cipher import AES

def encode(key, nonce, data):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    ciphertext = cipher.encrypt(data)
    
    return ciphertext

def decode(key, nonce, data):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    message = cipher.decrypt(data)

    return message

print("====================== CONFIG  ======================")
flag = 'HACK4U{435_(TR_I5_R3411Y_53(UR3}'
secret_message = '''
    You have decoded the base64 riddle. But you did not think this would be so easy, right? 
    Prepare yourself for the cryptic cipher ahead! Here is the tip:
    AES is the Algorithm
    COUNTER the Mode
    NONCE is In My Spanish Postal Code
    ZERO is the Padding
    and KEY is the name of my dog.
    If you solve this, you will be able to decrypt this: <FLAG>
'''
nonce = b'28001'
aes_key = b'HERCULES'.ljust(16, b'\x00')


# print(f"aes_key: {binascii.hexlify(aes_key)}")
# print(f"nonce: {binascii.hexlify(nonce)}")

crypted_flag = encode(aes_key, nonce, flag.encode())

# print(f"Base64 CypherText: {base64.b64encode(crypted_flag).decode()}")

with open('my_best_secret.txt', "wb") as f:
    f.write(base64.b64encode(secret_message.replace('<FLAG>', base64.b64encode(crypted_flag).decode()).encode()))