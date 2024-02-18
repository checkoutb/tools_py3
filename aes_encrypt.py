
import base64
from Crypto.Cipher import AES


# https://zhuanlan.zhihu.com/p/144316610


'''
AES对称加密算法
'''
# 需要补位，str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes
# 加密方法
def encrypt(key, text):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)  # 初始化加密器         # .. CBC更好一点，会加盐。 ECB，同一个明文生成的密文是不变的。
    encrypt_aes = aes.encrypt(add_to_16(text))  # 先进行aes加密
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    return encrypted_text
# 解密方法
def decrypt(key, text):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)  # 初始化加密器
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))  # 优先逆向解密base64成bytes
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')  # 执行解密密并转码返回str
    return decrypted_text


if __name__ == "__main__":
    key = "Fz1zzz##dd"
    value = "asdasdasd"
    encry = encrypt(key, value)
    print(encry)

    decry = decrypt(key, encry)
    print(decry)


    a = "asd中文asd"        # 主要是上面的 add_to_16, 最后进行 str.encode 后，中文会变为多个字节，导致不满足 16的倍数。
                            # ASCII的话，不会。
    print(str.encode(a))

    a = "asdasdasd!@#$32"
    print(str.encode(a))


