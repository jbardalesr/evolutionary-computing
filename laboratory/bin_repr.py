import math


def dec2bin(num: int, bits: int) -> list[int]:
    bin = [0] * bits
    index = 0
    while True:
        bin[index] = num % 2
        if num // 2 <= 0:
            break
        num = num // 2
        index += 1
    return bin[::-1]


def bin2dec(my_bin: list[int]) -> int:
    num = 0
    for i, b in enumerate(reversed(my_bin)):
        num = num + b * 2**i
    return num


def bin2gray(my_bin: list[int]) -> list[int]:
    my_gray = [my_bin[0]]
    for i in range(1, len(my_bin)):
        my_gray.append(my_bin[i - 1] ^ my_bin[i])
    return my_gray


def gray2bin(my_gray: list[int]) -> list[int]:
    # recursive version
    my_bin = [my_gray[0]]
    for k in range(1, len(my_gray)):
        my_bin.append(my_gray[k] ^ my_bin[k - 1])
    return my_bin


def show(my_bin):
    return "".join(str(e) for e in my_bin)


def my_map(x, a, b, epsilon) -> int:
    if a <= x and x <= b:
        u = round((x - a) / epsilon)
        return u
    return a if a < x else b


def inverse_map(u, a, epsilon) -> int:
    return u * epsilon + a
