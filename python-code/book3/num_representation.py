def dec2gray(num: int) -> int:
    return num ^ (num >> 1)


def gray2dec(gray: int) -> int:
    mask = gray
    while mask:
        mask >>= 1
        gray ^= mask
    return gray


print(gray2dec(dec2gray(28)))
