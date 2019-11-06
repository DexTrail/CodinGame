"""
Palindromic Decomposition
https://www.codingame.com/ide/puzzle/palindromic-decomposition

Version: 0.3
Created: 08/07/2019
Last modified: 08/07/2019
"""

import sys
import math
import time

# Main input
input_string = input()


def asymmetric(x: int, v: int) -> int:
    """ Asymmetric string """
    # res = 3 * x + (v - 3)
    return 3 * x + (v - 3)


def symmetric(x: int) -> int:
    """ Symmetric string """
    # n = x - 2
    # res = n * (n + 1) / 2
    # Total = Asymmetric + Symmetric
    n = x - 2
    return n * (n + 1) // 2


def general(string: str) -> int:
    """ General case (no patterns in the string) """
    result = 0
    length = len(string)
    for i in range(length):
        str1 = string[:i + 1]
        if len(set(str1)) == 1 or str1 == str1[::-1]:
            if i == length - 1:
                result += 3
                break

            for j in range(i + 1, length):
                str2 = string[i + 1:j + 1]
                if len(set(str2)) == 1 or str2 == str2[::-1]:
                    if j == length - 1:
                        result += 3
                        continue

                    str3 = string[j + 1:]
                    if len(set(str3)) == 1 or str3 == str3[::-1]:
                        result += 1
    return result


# Debug info
print("Input:", input_string, file=sys.stderr)
print("Length:", len(input_string), file=sys.stderr)

ts = time.perf_counter()

length = len(input_string)
result = 0
string = ''
x = 1
if len(set(input_string)) == 1:
    result = asymmetric(length, 3)
    if length >= 3:
        result += symmetric(length)
else:
    for i in range(length // 2):
        string += input_string[i]
        step = len(string)
        if length % step != 0:
            continue

        for j in range(i + 1, length - step + 1, step):
            if string != input_string[j:j + step]:
                x = 1
                break
            x += 1
        if x != 1:
            break
    else:
        string = input_string

    result = general(string)
    if x != 1:
        v = result
        result = asymmetric(x, v)
        if string == string[::-1]:
            result += symmetric(x)
            if string[:len(string) // 2 + 1] == string[len(string) // 2:]:
                result -= 1

te = time.perf_counter()

# Debug info
print("Result:", result, file=sys.stderr)
# print("general(input_string) =", general(input_string), file=sys.stderr)
print("Time: {:.3} input_string".format(te - ts), file=sys.stderr)

print(result)
