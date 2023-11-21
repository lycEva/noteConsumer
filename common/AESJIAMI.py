import base64
from Crypto.Cipher import AES


class Aesjiami:
    def aes_encry(self, data, key, iv):
        key = key.encode('utf-8')
        iv = iv.encode('utf-8')
        count = len(data.encode('utf-8'))
        # data不是16的倍数那就补足为16的倍数
        if count % 16 != 0:
            add = 16 - (count % 16)
        else:
            add = 0
        endata = data + (add * '*')

        aes = AES.new(key, AES.MODE_CBC, iv)   # 初始化加密器
        res = aes.encrypt(endata.encode('utf-8'))
        res1 = base64.b64encode(res)  # 通过base64转换成可处理的字节流数据
        return str(res1.decode('utf-8'))


if __name__ == '__main__':
    a_key = 'H9n&S@oGohGpV6d7'
    a_iv = '5150956153345366'
    Aesjiami().aes_encry('便签1', a_key, a_iv)
