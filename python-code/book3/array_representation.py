import copy
import random
import math


def dec2bin(num: int, max_value: int = None) -> list[int]:
    if max_value == None:
        max_value = num
    size = int(math.log2(max_value)) + 1
    bin = [0]*size
    index = 1
    while True:
        bin[size - index] = num % 2
        if num//2 <= 0:
            break
        num = num//2
        index += 1
    return bin


def bin2dec(my_bin: list[int]):
    num = 0
    for i, b in enumerate(reversed(my_bin)):
        num = num + b*2**i
    return num


def bin2gray(my_bin: list[int]) -> list[int]:
    my_gray = [my_bin[0]]
    for i in range(1, len(my_bin)):
        my_gray.append(my_bin[i - 1] ^ my_bin[i])
    return my_gray


def gray2bin(my_gray: list[int]) -> list[int]:
    my_bin = [my_gray[0]]
    for k in range(1, len(my_gray)):
        my_bin.append(my_gray[k] ^ my_bin[k - 1])
    return my_bin


print(bin2dec(gray2bin(bin2gray(dec2bin(256)))))
