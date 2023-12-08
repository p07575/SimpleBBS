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

def encrypt_data(msg,key):
    public_key = get_key(key)
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
    # print(type(public_key))
    verifier = PKCS1_signature.new(publick_key)
    digest = SHA.new()
    digest.update(text.encode("utf8"))
    return verifier.verify(digest, base64.b64decode(sign))

#加密
def rsa_encrypt(data,length=50):
    #导入公钥
    with open('tempRsa.pem') as f:
        # 拼接公钥的前后缀
        #key = '-----BEGIN RSA PRIVATE KEY-----\n' + f.read() + '\n-----END RSA PRIVATE KEY-----'
        key = f.read()
        # print(key)
        # 使用 RSA 的 importKey() 方法对(从文件中读取的)公钥字符串进行处理，处理成可用的加密公钥。
        pub_key = RSA.importKey(str(key))
        # 实例化一个加密对象 cipher ，传入的参数是公钥，通过 cipher 的 encrypt() 方法对信息进行加密。
        cipher = PKCS1_cipher.new(pub_key)
    # 对传入的数据data进行编码，
    data = data.encode()
    if len(data) <= length:
        # 对编码的数据进行加密，并通过base64进行编码
        result = base64.b64encode(cipher.encrypt(data))
    else :
        rsa_text = []
        # 对编码后的数据进行切片，原因：加密长度不能过长
        for i in range(0, len(data), length):
            cont = data[i:i + length]
            # 对切片后的数据进行加密，并新增到text后面
            rsa_text.append(cipher.encrypt(data))
        # 加密完进行拼接
        cipher_text = b''.join(rsa_text)
        # base64进行编码
        result = base64.b64encode(cipher_text)
    return result.decode()
 
#解密
def rsa_decrypt(data):
    with open('rsa_private_key.pem') as f:
        key = f.read()
        # 使用 RSA 的 importKey() 方法对(从文件中读取的)私钥字符串进行处理，处理成可用的加密公钥。
        pub_key = RSA.importKey(str(key))
        # 实例化一个加密对象 cipher ，传入的参数是私钥，通过 cipher 的 encrypt() 方法对信息进行加密。
        cipher = PKCS1_cipher.new(pub_key)
    # 对传入的数据data进行解码
    data=base64.b64decode(data)
    #解密
    result = cipher.decrypt(data,0)
    return result.decode('utf-8')
