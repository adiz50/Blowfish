import os
import base64
import numpy as np

P = [0x243f6a88, 0x85a308d3, 0x13198a2e, 0x03707344, 0xa4093822, 0x299f31d0, 0x082efa98, 0xec4e6c89, 0x452821e6,
     0x38d01377, 0xbe5466cf, 0x34e90c6c, 0xc0ac29b7, 0xc97c50dd, 0x3f84d5b5, 0xb5470917, 0x9216d5d9, 0x8979fb1b]

key = "0xfbda09182736c1d4"


def uploadSbox(sboxArray, src):
    counter = 0
    for fileName in os.listdir(src):
        if fileName.endswith(".txt"):
            file_path = f"{src}\{fileName}"
            file = open(file_path, "r")
            try:
                file = open(file_path, "r")
            except Exception:
                print("Can't find such file (wrong path)")
                return
            else:
                number = 0
                row = 0
                while True:
                    hexaString = file.read(8)
                    if not hexaString:
                        break
                    file.read(2)
                    number += 1
                    if number == 8:
                        file.read(1)
                        number = 0
                    sboxArray[row] = int(hexaString, base=16)
                    row += 1
            counter += 1
            file.close()
    return sboxArray


def divide_hexadecimal(hex_num):
    hex_num = hex_num.strip("0x")  # Remove '0x' prefix if present
    hex_num = hex_num.zfill(8)  # Pad with leading zeros if necessary

    return [int(hex_num[i:i + 2], 16) for i in range(0, 8, 2)]


def generateP():
    Pnew = np.empty(shape=18)
    key_parts = divide_hexadecimal(key)
    j = 0
    for (i, x) in enumerate(P):
        Pnew[i] = x ^ key_parts[j%18]
    return Pnew


def addMod32(a, b):
    return (a + b) % (2**32)


def functionF(value32):
    sboxArray = np.zeros((256, 4), dtype=float)
    sboxArray = uploadSbox(sboxArray, '.\s-blocks\sbox256x32bit')
    block8bits = [value32[i: i + 8] for i in range(0, len(value32), 8)]
    sboxVals = [sboxArray[int(block8bits[i], 2), i] for i in range(4)]
    add1 = addMod32(sboxVals[0], sboxVals[1])
    xor1 = int(add1) ^ int(sboxVals[2])
    addFinal = addMod32(xor1, int(sboxVals[3]))
    return format(addFinal, '032b')

def into64bit(M):
    num = (len(M)) // 8
    if len(M) % 8 != 0:  # pad with 0's
        num += 1
        M += '\0' * (8 - len(M) % 8)
    words = [M[i*8: (i*8) + 8] for i in range(num)]
    return [''.join(format((ord(o)), '08b') for o in i) for i in words]

def bitsToStr(B):
    wordsBits = [B[i:i+8] for i in range(0, len(B), 8)]
    words = [chr(int(i, 2)) for i in wordsBits]
    return ''.join(words)

def encryptionRound(value, i, subkeys):
    i = i % len(subkeys)
    firstpart, secondpart = value[:len(value) // 2], value[len(value) // 2:]
    L = int(firstpart, 2)
    R = int(secondpart, 2)
    # print(subkeys)
    L ^= int(subkeys[i])
    R ^= int(functionF(format(L, '032b')), 2)
    return  format(R, '032b') + format(L, '032b')

def postProcessing(roundsOutput, subkeys):
    x_left = int(roundsOutput[:32], 2) ^ int(subkeys[16])
    x_right = int(roundsOutput[32:], 2) ^ int(subkeys[17])
    return format(x_right, '032b') + format(x_left, '032b')

def preProcessing(roundsOutput, subkeys):
    x_left = int(roundsOutput[:32], 2) ^ int(subkeys[1])
    x_right = int(roundsOutput[32:], 2) ^ int(subkeys[0])
    return format(x_right, '032b') + format(x_left, '032b')

def encrypt(data):
    subkeys = generateP()
    data = into64bit(data)
    # print([data[0][i:8+i] for i in range(0, len(data[0]), 8)])
    result = []
    for x in data:
        for i in range(16):
            x = encryptionRound(x, i, subkeys)
        x = postProcessing(x, subkeys)
        result.append(x)
    return result


def decrypt(data):
    subkeys = generateP()
    # subkeys = np.flip(subkeys)
    data = into64bit(data)
    result = []
    for x in data:
        for i in range(17, 1, -1):
            x = encryptionRound(x, i, subkeys)
        x = preProcessing(x, subkeys)
        result.append(x)
    return result

def inputPostProcessing(data):
    return data.replace('\0', '')

def main():
    # https://www.geeksforgeeks.org/blowfish-algorithm-with-examples/
    # https://www.tutorialspoint.com/how-are-subkeys-generated-in-blowfish-algorithm
    #sboxArray = np.zeros((256, 4), dtype=float)
    #sboxArray = uploadSbox(sboxArray, '.\s-blocks\sbox256x32bit')
    data = "bigdataprojekt3242904jg0g92kkegdofg::efefef"
    print(data)
    encrypted = bitsToStr(''.join(encrypt(data)))
    encryptedBase64 = base64.b64encode(encrypted.encode('utf-8')).decode('utf-8')
    print(encryptedBase64)
    decrypted = bitsToStr(''.join(decrypt(encrypted)))
    print(inputPostProcessing(decrypted))



if __name__ == '__main__':
    main()
