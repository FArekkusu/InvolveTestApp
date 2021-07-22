from hashlib import sha256

def generate_signature(source_string):
    return sha256(bytes(source_string, encoding="utf-8")).hexdigest()


def normalize_number(number):
    if "." not in number:
        number += ".00"
    if number[-2] == ".":
        number += "0"
    return number