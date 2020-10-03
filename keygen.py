#!/usr/bin/env python3

import hashlib
import itertools as it
import random
from typing import Iterable

BASE30 = "123456789ABCDEFGHJKLMNPQRTVWXY"


def last_bits(number: int, n: int) -> int:
    return number & ((1 << n) - 1)


def group(iterable, size: int, fill=None):
    """Groups iterable in tuples"""
    yield from it.zip_longest(*(iter(iterable),) * size, fillvalue=fill)


def to_b30(number: int) -> str:
    """Converts number to base30"""
    res = ""
    while number:
        number, digit = divmod(number, 30)
        res += BASE30[digit]

    return res[::-1]


def add_hyphens(code: Iterable[str], n: int = 5) -> str:
    return "-".join("".join(i) for i in group(code, n, ""))


def loop(ecx: int, chars: Iterable[str]) -> int:
    part = 0
    for c in chars:
        part *= ecx
        part += ord(c)
    return part & ((1 << 20) - 1)


def license_hash(license: str, request: str) -> str:
    hasher = hashlib.sha1()
    hasher.update(request.encode("ascii"))
    hasher.update(license.encode("ascii"))
    return add_hyphens(
        request[:3] + to_b30(int(hasher.hexdigest().upper()[::2], 16)).rjust(17, "1")
    )


def activation_code(lichash: str) -> str:
    return add_hyphens(
        "AXX"
        + to_b30(
            sum(loop(j, lichash) << i * 20 for i, j in enumerate((27, 93, 13, 221)))
        ).ljust(17, "1")
    )


def interactive():
    license_id = add_hyphens(
        it.chain("CN", random.choices("123456789ABCDEFGHJKLMNPQRTVWXY", k=18))
    )
    print("License id:", license_id)
    request_code = input("Enter request code: ").strip()

    print("Activation code:", activation_code(license_hash(license_id, request_code)))


if __name__ == "__main__":
    interactive()
