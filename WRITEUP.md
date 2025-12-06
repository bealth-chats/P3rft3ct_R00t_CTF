# P3rft3ct_R00t_CTF Solution

## Challenge Description
The challenge provided two contract addresses on the Sepolia network:
- `0xf1000945300874d8FFe6392FBEdFBB1279B6E55f`
- `0x3dCa65b7546ed94c81730B9b0C133A753446756e`

The hint suggested: "Two signatures. One hand. A hidden truth. Uncover what the signer never intended to reveal." and "Some roots are meant to be shared, but others remain perfect secrets."

## Investigation
By inspecting the source code of the first contract (which the second one also matches), we found that they are `TxEmitter` contracts. These contracts simply store chunks of bytes that can be concatenated to form a raw RLP-encoded signed transaction.

## Solution

1. **Fetching the Data**: We used a Python script to interact with the contracts on the Sepolia network and fetch the transaction data using the `getAll()` function.

2. **Decoding the Transactions**: The fetched data was identified as Legacy transactions (RLP list). We decoded the RLP data to extract the transaction fields.

3. **Extracting Signatures**: From the decoded transactions, we extracted the `r`, `s`, and `v` values of the ECDSA signature. We also reconstructed the message hash `z` by RLP-encoding the transaction fields (excluding the signature) and hashing it with Keccak-256.

4. **Identifying the Vulnerability**: Upon inspection, we noticed that both transactions had the **same `r` value**:
   ```
   r: 0x1456198d457b6a4bb1c624d35f62a96eb1d2981e89dd2c045823b1a37dcc3370
   ```
   This indicates **nonce reuse**. The same random nonce $k$ was used to sign two different messages. In ECDSA, if $k$ is reused, the private key $d$ can be recovered.

5. **Recovering the Private Key**:
   Using the formula:
   $$ k = (z_1 - z_2) * (s_1 - s_2)^{-1} \pmod n $$
   $$ d = r^{-1} * (s_1 * k - z_1) \pmod n $$

   Where $n$ is the order of the secp256k1 curve.

   We calculated $d$ and recovered the private key.

## Flag
The recovered private key is `0xbebdb993f1033066fcb07f07d425d8a628e3c0bcbdd5ccc748d7626b7e53684`.

**Flag:** `r00t{0xbebdb993f1033066fcb07f07d425d8a628e3c0bcbdd5ccc748d7626b7e53684}`
