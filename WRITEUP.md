# Challenge Writeup

## Challenge Description
Find the flag hidden in a contract deployment on Sepolia Testnet.
Transaction Hash: `0xa9179ed7e17db0868e2676af77bb25a46b5adc934e0bc361a7057c1df5eaa118`
Flag Format: `r00t{YY-MM-DD_HH:MM:SS_Addr_blockNumber}`
- Timestamp in EAT (UTC+3)
- Addr: Last 3 hex chars of deployer address
- blockNumber: Block number of deployment

## Solution Process

1.  **Analyze the Transaction**:
    Using a Sepolia RPC (`https://1rpc.io/sepolia`), I fetched the transaction details for `0xa9179ed7e17db0868e2676af77bb25a46b5adc934e0bc361a7057c1df5eaa118`.

2.  **Extract Data**:
    -   **Deployer Address**: `0x44203E9DdBd65a544F4abA5372F7D4a0cDcDE2aC`
    -   **Block Number**: `9398687`

3.  **Uncover Hidden Timestamp**:
    The challenge description mentions "the exact timestamp hidden in the contract's creation data".
    Analyzing the input data (bytecode + arguments) of the transaction, I found encoded arguments at the end of the input string.
    The last two 32-byte words are:
    1.  `000000000000000000000000000000000000000000000000000000006916c6b9`
    2.  `00000000000000000000000023618e81e3f5cdf7f54c3d65f7fbc0abf5b21f01`

    The first word `0x6916c6b9` corresponds to the decimal value `1763100345`.
    Checking this value as a Unix timestamp:
    -   UTC: `2025-11-14 06:05:45`
    This matches the context of a "secret" deployment time.

4.  **Process Data**:
    -   **Timestamp Conversion**: The challenge requires EAT (East Africa Time), which is UTC+3.
        -   UTC: `2025-11-14 06:05:45`
        -   EAT: `2025-11-14 09:05:45`
        -   Formatted: `25-11-14_09:05:45`
    -   **Address Fragment**: Last 3 chars of `0x44203E9DdBd65a544F4abA5372F7D4a0cDcDE2aC` are `2aC`.

5.  **Construct Flag**:
    Combining the parts: `r00t{25-11-14_09:05:45_2aC_9398687}`

## Script
A python script `solve_challenge.py` was used to automate the extraction and formatting.

## Flag
`r00t{25-11-14_09:05:45_2aC_9398687}`
