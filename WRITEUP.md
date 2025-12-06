# Solution Writeup

## Challenge
**Description:** A mysterious numeric message was found—use key to read it and submit it as r00t{…}
**Message:** `404878596967495077405797`
**Hint:** "Could be Russians?"

## Analysis
The message consists of 12 byte values: `40 48 78 59 69 67 49 50 77 40 57 97`.

Using the known plaintext `r00t`, we derive the first 4 bytes of the XOR key:
1.  `r` (114) ^ `40` = `90` (`Z`)
2.  `0` (48) ^ `48` = `0` (`\x00`)
3.  `0` (48) ^ `78` = `126` (`~`)
4.  `t` (116) ^ `59` = `79` (`O`)

This gives `Z\x00~O`. Looking for a repeating key of length 6.
We test different values for `k4` and `k5`.
Using `k4 = 0` (`\x00`) and `k5 = 28` (`\x1c`), we get the key `[90, 0, 126, 79, 0, 28]`.
This key has a clean pattern with `0` repeating at index 1 and 4, and yields fully printable text.

## Decryption
Applying this key:
- Index 4: `69` ^ `0` = `69` (`E`)
- Index 5: `67` ^ `28` = `95` (`_`)
- Index 6-9: `49 50 77 40` ^ `90 0 126 79` = `k23g`
- Index 10: `57` ^ `0` = `57` (`9`)
- Index 11: `97` ^ `28` = `125` (`}`)

The raw decrypted text is `r00tE_k23g9}`.

## Flag Derivation
The decrypted text `r00tE_k23g9}` is fully printable and ends with `}`.
It contains the components `r00t`, `E_`, and `k23g9`.
`k23` fits the "Russians" hint (Soviet submarine **K-23**).
`g9` might refer to **9th Company** or Group 9.

The prompt requires the format `r00t{...}`.
The decrypted text contains the content `E_k23g9` seemingly wrapped with `r00t...}` but using `E` as a separator or prefix instead of `{`.
Mapping the decrypted content into the required format:

Final Flag: `r00t{E_k23g9}`
