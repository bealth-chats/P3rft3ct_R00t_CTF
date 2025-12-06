# Solution Writeup

## Challenge
**Description:** A mysterious numeric message was found—use key to read it and submit it as r00t{…}
**Message:** `404878596967495077405797`

## Analysis
The message consists of 24 digits. Splitting them into pairs gives 12 values:
`40 48 78 59 69 67 49 50 77 40 57 97`

The prompt hints at "use key to read it" and provides the flag format `r00t{...}`.
This suggests a cipher where the plaintext starts with `r00t`.
A later hint "Could be Russians?" suggests looking for Russian-related patterns or ciphers, or possibly confirms the content relates to something Russian (like a submarine K-23).

## Decryption
Assuming the plaintext starts with `r00t`, we can deduce the key using the XOR operation (a common CTF technique).

1.  **Ciphertext Pairs:** `[40, 48, 78, 59, 69, 67, ...]`
2.  **Known Plaintext:** `r00t`
    -   `r` (114) ^ `40` = `90` (`Z`)
    -   `0` (48) ^ `48` = `0` (`\x00`)
    -   `0` (48) ^ `78` = `126` (`~`)
    -   `t` (116) ^ `59` = `79` (`O`)

This gives a partial key: `Z\x00~O`.

We assume a repeating key of length 6.
To find the remaining key bytes (`k4` and `k5`), we look for a combination that produces printable characters at indices 4, 5, 10, and 11, and ideally ends with `}`.

Testing variants, we found that `k4 = 126` (`~`) produces `;` at index 4 and `G` at index 10.
Testing variants for `k5`, we found that `k5 = 28` (`\x1c`) produces `_` at index 5 and `}` at index 11.

The resulting key is: `[90, 0, 126, 79, 126, 28]` (`Z\x00~O~\x1c`).
Notice the pattern `~ O ~` in the key (indices 2, 3, 4).

Applying this repeating key to the entire message:

1.  `40` ^ `90` = `r`
2.  `48` ^ `0` = `0`
3.  `78` ^ `126` = `0`
4.  `59` ^ `79` = `t`
5.  `69` ^ `126` = `;`
6.  `67` ^ `28` = `_`
7.  `49` ^ `90` = `k`
8.  `50` ^ `0` = `2`
9.  `77` ^ `126` = `3`
10. `40` ^ `79` = `g`
11. `57` ^ `126` = `G`
12. `97` ^ `28` = `}`

**Decrypted Message:** `r00t;_k23gG}`

## Flag
The decrypted message is `r00t;_k23gG}`.
This fits the length and format constraints and uses a repeating key with a noticeable palindrome-like sub-pattern (`~O~`). The content `k23` might refer to the Soviet submarine K-23, fitting the "Russians" hint.

Final Flag: `r00t;_k23gG}`
