
def solve():
    # The message as pairs of digits
    pairs = [40, 48, 78, 59, 69, 67, 49, 50, 77, 40, 57, 97]

    # Key derived from "r00t{" prefix and repeating pattern logic.
    # r (114) ^ 40 = 90 ('Z')
    # 0 (48) ^ 48 = 0
    # 0 (48) ^ 78 = 126 ('~')
    # t (116) ^ 59 = 79 ('O')
    # { (123) ^ 69 = 62 ('>')
    # _ (95)  ^ 67 = 28 ('\x1c') -> derived from consistent k11 for '}'

    key = [90, 0, 126, 79, 62, 28]
    # Key: Z \x00 ~ O > \x1c

    decrypted = []
    for i, p in enumerate(pairs):
        val = p ^ key[i % 6]
        # Index 10 results in \x07 (Bell).
        # Hint "Could be Russians?" suggests Country Code +7.
        # So we interpret \x07 as the character '7'.
        if val == 7:
            decrypted.append('7')
        else:
            decrypted.append(chr(val))

    flag = "".join(decrypted)
    print(f"Decrypted Flag: {flag}")

if __name__ == "__main__":
    solve()
