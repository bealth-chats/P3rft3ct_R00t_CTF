from web3 import Web3
from datetime import datetime, timezone, timedelta
import sys

# List of public RPCs to try
rpcs = [
    'https://rpc.sepolia.org',
    'https://1rpc.io/sepolia',
    'https://sepolia.drpc.org'
]

w3 = None
for rpc in rpcs:
    print(f"Trying to connect to {rpc}...")
    temp_w3 = Web3(Web3.HTTPProvider(rpc))
    if temp_w3.is_connected():
        w3 = temp_w3
        print(f"Connected to {rpc}")
        break
    else:
        print(f"Failed to connect to {rpc}")

if not w3:
    print("Could not connect to any Sepolia RPC")
    sys.exit(1)

tx_hash = '0xa9179ed7e17db0868e2676af77bb25a46b5adc934e0bc361a7057c1df5eaa118'

print(f"Fetching transaction {tx_hash}...")
try:
    # Get transaction
    tx = w3.eth.get_transaction(tx_hash)
except Exception as e:
    print(f"Error fetching transaction: {e}")
    sys.exit(1)

# Get deployer address (from)
deployer_address = tx['from']
print(f"Deployer Address: {deployer_address}")

# Get block number
block_number = tx['blockNumber']
print(f"Block Number: {block_number}")

# Get block
print(f"Fetching block {block_number}...")
block = w3.eth.get_block(block_number)
timestamp = block['timestamp']
print(f"Timestamp (UTC): {timestamp}")

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
