import base64
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
 
def gen_key():
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)
    # 生成私钥
    private_key = rsa.exportKey()
    # 生成公钥
    public_key = rsa.publickey().exportKey()
    
    with open('rsa_private_key.pem', 'wb')as f:
        f.write(private_key)
        
    with open('rsa_public_key.pem', 'wb')as f:
        f.write(public_key)

def get_key(key_file):
    with open(key_file) as f:
        data = f.read()
        # print(type(data))
        key = RSA.importKey(data)

    return key

def encrypt_data(msg):
    public_key = get_key('rsa_public_key.pem')
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
    return encrypt_text.decode('utf-8')

def decrypt_data(encrypt_msg):
    private_key = get_key('rsa_private_key.pem')
    cipher = PKCS1_cipher.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)
    return back_text.decode('utf-8')

def rsa_private_sign(data):
    private_key = get_key('rsa_private_key.pem')
    signer = PKCS1_signature.new(private_key)
    digest = SHA.new()
    digest.update(data.encode("utf8"))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    signature = signature.decode('utf-8')
    return signature

def rsa_public_check_sign(text, sign, key):
    publick_key = get_key(key)
    # print(type(publick_key))
    verifier = PKCS1_signature.new(publick_key)
    digest = SHA.new()
    digest.update(text.encode("utf8"))
    return verifier.verify(digest, base64.b64decode(sign))