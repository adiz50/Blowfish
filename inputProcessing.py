def into64bit(M):
    num = len(M) // 8

    if len(M) % 8 != 0:  # pad with 0's
        num += 1
        M += '0' * (8 - len(M) % 8)

    words = [M[i*8: (i+1) * 8] for i in range(num)]
    wordsBit = []

    return [''.join(format((ord(o)), '08b') for o in i) for i in words]
