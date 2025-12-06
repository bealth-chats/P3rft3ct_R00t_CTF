# Solution Writeup

## Challenge
**Description:** A mysterious numeric message was found—use key to read it and submit it as r00t{…}
**Message:** `404878596967495077405797`
**Hint:** "Could be Russians?"

## Analysis
The message consists of 12 byte values: `40 48 78 59 69 67 49 50 77 40 57 97`.

The flag format `r00t{...}` allows us to derive the beginning of the key using XOR.
1.  `r` (114) ^ `40` = `90` (`Z`)
2.  `0` (48) ^ `48` = `0` (`\x00`)
3.  `0` (48) ^ `78` = `126` (`~`)
4.  `t` (116) ^ `59` = `79` (`O`)
5.  `{` (123) ^ `69` = `62` (`>`)

This gives a partial key `Z\x00~O>`. Assuming the key repeats every 6 bytes:
6.  `_` (95) ^ `67` = `28` (`\x1c`)
    - We check this key byte against the last character (index 11).
    - `97` ^ `28` = `125` (`}`), which fits the flag format perfectly.

So the key is `[90, 0, 126, 79, 62, 28]`.

## Decryption
Applying the key to the ciphertext:
- Index 0-5: `r00t{_`
- Index 6: `49` ^ `90` = `107` (`k`)
- Index 7: `50` ^ `0` = `50` (`2`)
- Index 8: `77` ^ `126` = `51` (`3`)
- Index 9: `40` ^ `79` = `103` (`g`)
- Index 10: `57` ^ `62` = `7` (`\x07`)
- Index 11: `97` ^ `28` = `125` (`}`)

Raw Decryption: `r00t{_k23g\x07}`.

The character at index 10 is `\x07` (Bell), which is non-printable.
The hint "Could be Russians?" suggests a connection to Russia.
The value `7` corresponds to the international dialing code for Russia (**+7**).
Therefore, we interpret the value `7` as the character `7`.

## Flag
Replacing `\x07` with `7`:
`r00t{_k23g7}`

Final Flag: `r00t{_k23g7}`
