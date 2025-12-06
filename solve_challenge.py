from web3 import Web3
from datetime import datetime, timezone, timedelta
import sys

# Connect to RPC
rpc = 'https://1rpc.io/sepolia'
w3 = Web3(Web3.HTTPProvider(rpc))

if not w3.is_connected():
    print("Failed to connect")
    sys.exit(1)

tx_hash = '0xa9179ed7e17db0868e2676af77bb25a46b5adc934e0bc361a7057c1df5eaa118'
print(f"Fetching transaction {tx_hash}...")
tx = w3.eth.get_transaction(tx_hash)

# Get deployer address (from)
deployer_address = tx['from']
print(f"Deployer Address: {deployer_address}")

# Get block number
block_number = tx['blockNumber']
print(f"Block Number: {block_number}")

# Analyze input data for hidden timestamp
input_data = tx['input']
# Constructor arguments are usually at the end.
# Based on analysis, the last 64 bytes (2 words) contain data.
# The timestamp is likely the first of these two words (offset -64 to -32).
# Word 1: 0x6916c6b9 -> 1763100345

timestamp_hex = input_data[-64:-32].hex()
timestamp = int(timestamp_hex, 16)
print(f"Hidden Timestamp (Decimal): {timestamp}")

# Verify if it looks like a valid timestamp (approx 2025)
# 1763100345 is indeed around Nov 2025.

# Convert timestamp to EAT (UTC+3)
utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
eat_offset = timedelta(hours=3)
eat_time = utc_time + eat_offset

print(f"Time (EAT): {eat_time}")

# Flag Format: r00t{YY-MM-DD_HH:MM:SS_Addr_blockNumber}
# Addr represents the last 3 hexadecimal characters of the deployer address.

addr_suffix = deployer_address[-3:]

formatted_time = eat_time.strftime('%y-%m-%d_%H:%M:%S')

flag = f"r00t{{{formatted_time}_{addr_suffix}_{block_number}}}"
print(f"Flag: {flag}")

with open("flag.txt", "w") as f:
    f.write(flag)
