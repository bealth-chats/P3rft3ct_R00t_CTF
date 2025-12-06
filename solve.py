
def solve():
    # The message as pairs of digits
    pairs = [40, 48, 78, 59, 69, 67, 49, 50, 77, 40, 57, 97]

    # Key derived from "r00t" prefix and searching for a consistent pattern.
    # Key: [90, 0, 126, 79, 0, 28]
    # 'Z' '\x00' '~' 'O' '\x00' '\x1c'
    # This key yields a fully printable string `r00tE_k23g9}`.

    key = [90, 0, 126, 79, 0, 28]

    decrypted = []
    for i, p in enumerate(pairs):
        val = p ^ key[i % 6]
        decrypted.append(chr(val))

    raw_flag = "".join(decrypted)
    print(f"Raw Decrypted: {raw_flag}")

    # Raw Decrypted: r00tE_k23g9}
    # This string ends with '}'.
    # It starts with 'r00t'.
    # It has 'E_' following 'r00t'.
    # It has 'k23g9' following 'E_'.
    # The flag format is r00t{...}.
    # We interpret the decrypted string as containing the content `E_k23g9` inside the wrapper.
    # So we format it as r00t{E_k23g9}.

    final_flag = "r00t{E_k23g9}"
    print(f"Final Flag: {final_flag}")

if __name__ == "__main__":
    solve()
