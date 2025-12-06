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
    -   **Block Timestamp (UTC)**: `1760306256` (which corresponds to `2025-10-12 21:57:36 UTC`)

3.  **Process Data**:
    -   **Timestamp Conversion**: The challenge requires EAT (East Africa Time), which is UTC+3.
        -   UTC: `2025-10-12 21:57:36`
        -   EAT: `2025-10-13 00:57:36`
        -   Formatted: `25-10-13_00:57:36`
    -   **Address Fragment**: Last 3 chars of `0x44203E9DdBd65a544F4abA5372F7D4a0cDcDE2aC` are `2aC`.

4.  **Construct Flag**:
    Combining the parts: `r00t{25-10-13_00:57:36_2aC_9398687}`

## Script
A python script `solve_challenge.py` was used to automate the extraction and formatting.

## Flag
`r00t{25-10-13_00:57:36_2aC_9398687}`
