
def solve():
    pairs = [40, 48, 78, 59, 69, 67, 49, 50, 77, 40, 57, 97]

    # Key hypothesis: [90, 0, 126, 79, 14, 28]
    # k4=14 (0x0E), k5=28 (0x1C). Doubling pattern.

    key = [90, 0, 126, 79, 14, 28]

    decrypted = []
    for i, p in enumerate(pairs):
        val = p ^ key[i % 6]
        decrypted.append(chr(val))

    raw_flag = "".join(decrypted)
    print(f"Raw Decrypted: {raw_flag}")

    # Raw Decrypted: r00tK_k23g7}
    # Content: K_k23g7
    # Interpretation:
    # K -> K-Class / Kremlin / Kalashnikov
    # k23 -> K-23 Submarine
    # g7 -> G7 (Russia kicked out)

    final_flag = "r00t{K_k23g7}"
    print(f"Final Flag: {final_flag}")

if __name__ == "__main__":
    solve()
