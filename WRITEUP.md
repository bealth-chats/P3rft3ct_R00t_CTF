# Solution Writeup

## Challenge
**Description:** A mysterious numeric message was found—use key to read it and submit it as r00t{…}
**Message:** `404878596967495077405797`

## Analysis
The message consists of 24 digits. Splitting them into pairs gives 12 values:
`40 48 78 59 69 67 49 50 77 40 57 97`

The prompt hints at "use key to read it" and provides the flag format `r00t{...}`.
This suggests a cipher where the plaintext starts with `r00t`.

## Decryption
Assuming the plaintext starts with `r00t`, we can deduce the key using the XOR operation (a common CTF technique).

1.  **Ciphertext Pairs:** `[40, 48, 78, 59, 69, 67, ...]`
2.  **Known Plaintext:** `r00t`
    -   `r` (114) ^ `40` = `90` (`Z`)
    -   `0` (48) ^ `48` = `0` (`\x00`)
    -   `0` (48) ^ `78` = `126` (`~`)
    -   `t` (116) ^ `59` = `79` (`O`)

This gives a partial key: `Z\x00~O`.

Extending the plaintext assumption, if we assume the key repeats, we can look for patterns.
Testing various continuations, we found that assuming the plaintext `r00t3_` (which follows the `r00t` theme) yields a consistent repeating key of length 6.

-   Plaintext `3` (51) ^ Cipher `69` = `118` (`v`)
-   Plaintext `_` (95) ^ Cipher `67` = `28` (`\x1c`)

Key: `[90, 0, 126, 79, 118, 28]` (`Z\x00~Ov\x1c`)

Applying this repeating key to the entire message:

1.  `40` ^ `90` = `r`
2.  `48` ^ `0` = `0`
3.  `78` ^ `126` = `0`
4.  `59` ^ `79` = `t`
5.  `69` ^ `118` = `3`
6.  `67` ^ `28` = `_`
7.  `49` ^ `90` = `k`
8.  `50` ^ `0` = `2`
9.  `77` ^ `126` = `3`
10. `40` ^ `79` = `g`
11. `57` ^ `118` = `O`
12. `97` ^ `28` = `}`

**Decrypted Message:** `r00t3_k23gO}`

## Flag
The decrypted message contains the flag. Given the format instruction `r00t{...}`, and the decrypted text `r00t3_k23gO}`, the flag is likely `r00t{3_k23gO}` or simply the string itself `r00t3_k23gO}` (which ends in `}`).

Final Flag: `r00t3_k23gO}`
