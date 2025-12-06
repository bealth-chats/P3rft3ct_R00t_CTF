# CTF Writeup: The Silent Vault

## Challenge Description
The challenge provides a contract address on the Sepolia Testnet (`0xD702054866DEA4840ab36D4f222C757a3349c422`) and the bytecode instructions. The goal is to find the exact `msg.value` that makes the vault open.

## Analysis

### 1. Disassembling
We disassembled the bytecode to understand the logic. The relevant part of the code is:

```assembly
0041: JUMPDEST
0042: PUSH1 0x20
0044: CALLDATASIZE
0045: EQ
0046: PUSH1 0x4c
0048: JUMPI
...
004c: JUMPDEST
004d: PUSH30 0x346e346c797a316e675f62797433633064335f6c316b335f345f70723000
006c: PUSH0
006d: MSTORE
006e: PUSH1 0x1e
0070: PUSH0
0071: SHA3
0072: CALLVALUE
0073: DUP2
0074: SLOAD
0075: EQ
0076: PUSH1 0x7c
0078: JUMPI
```

**Logic Breakdown:**
1. **Check Calldata Size**: The code requires `msg.data` length to be exactly 32 bytes.
2. **Push Value**: It pushes a 30-byte value `0x34...00` (which is the hex encoding of `4n4lyz1ng_byt3c0d3_l1k3_4_pr0\x00`).
3. **Store in Memory**: It executes `MSTORE(0, value)`. `PUSH30` left-pads the value with 2 zero bytes on the stack.
   - Memory becomes: `00 00 34 6e ... 72 30 00`.
4. **Calculate Hash**: It executes `SHA3(0, 30)`. This hashes the first 30 bytes of memory:
   - Input: `00 00 34 6e ... 72`. (It misses the last `0` and `\0`).
5. **Check Storage**: It loads the value from storage at this hash and compares it with `msg.value`.

### 2. The Discrepancy (Bug)
The logic described above hashes a byte sequence that starts with `00 00` and ends with `...pr`. The hash of this sequence corresponds to storage slot `0xb77ed8df0c9bccb800f70c61b747d97ab9741319cd6f0b3b5762e91438d34a44`.
We queried this slot on the Sepolia network and found it is **empty** (`0x0`).

However, if we hash the *clean* string `4n4lyz1ng_byt3c0d3_l1k3_4_pr0` (without the padding introduced by the runtime code), we get slot `0x47d34f5b68ee0923afd1e5cdc53211fd27be3332134da08878f3e53fac89721b`.
Querying this slot returns a secret value: `0x406de73ad7a8137c0` (4642542409869375424).

It appears the author intended to check against this secret, but the runtime assembly code is buggy (due to `PUSH30` padding and memory alignment) and checks the wrong slot.

### 3. Conclusion
The question asks for the **exact msg.value that makes the vault open**.
Since the runtime code checks against an empty slot (value 0), the `msg.value` must be `0` to satisfy the equality check (`0 == 0`) and trigger the "open" path.

While the "secret" value `4642542409869375424` exists in the contract, sending it as `msg.value` would cause the transaction to revert because the code does not check the slot where this secret is stored.

**Flag:** `r00t{0}`
