def dec2bin(dec):
    return bin(dec).replace("0b", "")


def bin2gray(b_str: str) -> str:
    n_bits = len(b_str)

    gc_str = b_str[0]  # string containing the binary representation
    for i in range(1, n_bits):
        gc_str += str(int(b_str[i - 1]) ^ int(b_str[i]))

    return gc_str


def gray2bin(gc_str: str) -> str:
    n_bits = len(gc_str)

    b_str = gc_str[0]
    for k in range(1, n_bits):
        if int(gc_str[k] == '0'):
            b_str += b_str[k-1]
        else:
            b_str += str((int(b_str[k-1]) + 1) % 2)
    return b_str


print(gray2bin("000011100"))
