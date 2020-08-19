#!/usr/bin/env python3

import string
import random
import hashlib  # sha ~> hashlib.sha1

BASE16 = "0123456789ABCDEF"
BASE30 = "123456789ABCDEFGHJKLMNPQRTVWXY"


def random_string(size=20, chars=string.ascii_uppercase + string.digits):
    return "".join((random.choice(chars) for _ in range(size)))


def base_convert(number, fromdigits, todigits, ignore_negative=True):

    len_todigits = int(len(todigits))  # Memo this...

    if not ignore_negative and str(number)[0] == "-":
        number = str(number)[1:]
        neg = 1
    else:
        neg = 0

    x = int(0)
    for digit in str(number):
        x = x * len(fromdigits) + fromdigits.index(digit)

    res = ""
    while x > 0:
        digit = x % len_todigits  # ... use memo'd
        res = todigits[digit] + res
        x //= len_todigits  # ... use memo'd | Mind the integer division!

    if neg:
        res = "-" + res

    return res


def add_hyphens(code):
    return code[:5] + "-" + code[5:10] + "-" + code[10:15] + "-" + code[15:]


def to16(hex_string):  # Reuse this code block, making it a function
    while len(hex_string) < 17:
        hex_string = "1" + hex_string
    return hex_string


def sha_to_base30(digest):
    tdigest = "".join(
        [c for i, c in enumerate(digest) if i // 2 * 2 == i]
    )  # Mind the integer division!
    result = base_convert(tdigest, BASE16, BASE30)
    return to16(result)  # Indeed, reused (1)


def loop(ecx, loopy_lichash):  # De-shadow outer scope variable
    part = 0
    for c in loopy_lichash:
        part = ecx * part + ord(c) & 1048575
    return part


def main():
    print("")
    rng = add_hyphens("CN" + random_string(18, "123456789ABCDEFGHJKLMNPQRTVWXY"))
    print("License id: " + rng)
    act30 = str(input("Enter request code: "))  # Emulate old raw_input
    lichash = act30
    hasher = hashlib.sha1()  # Call the constructor directly
    hasher.update(act30.encode())  # "Emulate" old sha.update(str)
    hasher.update(rng.encode())  # "Emulate" old sha.update(str)
    lichash = add_hyphens(lichash[:3] + sha_to_base30(hasher.hexdigest().upper()))
    part5 = (
        format(loop(221, lichash), "05x")
        + format(loop(13, lichash), "05x")
        + format(loop(93, lichash), "05x")
        + format(loop(27, lichash), "05x")
    )

    part5 = base_convert(part5.upper(), BASE16, BASE30)
    part5 = to16(part5)  # Indeed, reused (2)

    part5 = "AXX" + part5
    print("Activation code: " + add_hyphens(part5))
    print("")


if __name__ == "__main__":
    main()
