import sys

import numpy as np

P = [0x243f6a88, 0x85a308d3, 0x13198a2e, 0x03707344, 0xa4093822, 0x299f31d0, 0x082efa98, 0xec4e6c89, 0x452821e6,
     0x38d01377, 0xbe5466cf, 0x34e90c6c, 0xc0ac29b7, 0xc97c50dd, 0x3f84d5b5, 0xb5470917, 0x9216d5d9, 0x8979fb1b]


def getSbox(sboxArray, src):
    try:
        file = open(src, "rb")
    except:
        print("Can't find such file (wrong path)")
    else:
        row = 0
        while True:
            byte = file.read(1)
            file.seek(1, 1)
            if not byte:
                break

            sboxArray[row] = int.from_bytes(byte, byteorder=sys.byteorder)
            row += 1
        file.close()


def cipherUsingP(data):
    data = np.array(data)
    encrypted = np.empty(data.shape, dtype=data.dtype)
    i = 0
    for (x, j) in enumerate(data):
        encrypted[j] = P[i]^data[j]
        if i == len(P)-1:
            i = 0
        else:
            i += 1
    return encrypted


def encryptImage(sbox):
    return


def decryptImage(sbox):
    return


def main():
    # https://www.geeksforgeeks.org/blowfish-algorithm-with-examples/
    # https://www.tutorialspoint.com/how-are-subkeys-generated-in-blowfish-algorithm
    sboxArray = np.zeros(256, dtype=int)
    getSbox(sboxArray, '.\s-blocks\sbox_08x08_20130117_030729__Original.SBX')
    # print(sboxArray)
    encryptImage(sboxArray)
    decryptImage(sboxArray)


if __name__ == '__main__':
    main()
