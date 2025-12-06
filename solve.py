
def solve():
    # The message as pairs of digits
    pairs = [40, 48, 78, 59, 69, 67, 49, 50, 77, 40, 57, 97]

    # Key derived from analysis (XOR with "r00t" and pattern matching)
    # Key length 6 repeating
    key = [90, 0, 126, 79, 118, 28]

    decrypted = []
    for i, p in enumerate(pairs):
        decrypted.append(chr(p ^ key[i % 6]))

    flag = "".join(decrypted)
    print(f"Decrypted Flag: {flag}")

if __name__ == "__main__":
    solve()
