import web3
from web3 import Web3
from eth_account import Account
from eth_utils import keccak
import rlp

# Connect to Sepolia
# I will use a public RPC for now.
rpc_url = "https://1rpc.io/sepolia"
w3 = Web3(Web3.HTTPProvider(rpc_url))

if not w3.is_connected():
    print("Failed to connect to RPC")
    exit(1)

print("Connected to Sepolia")

# Contract addresses
contract_address_1 = "0xf1000945300874d8FFe6392FBEdFBB1279B6E55f"
contract_address_2 = "0x3dCa65b7546ed94c81730B9b0C133A753446756e"

# ABI for getAll
abi = [
    {
        "inputs": [],
        "name": "getAll",
        "outputs": [{"internalType": "bytes", "name": "full", "type": "bytes"}],
        "stateMutability": "view",
        "type": "function"
    }
]

contract1 = w3.eth.contract(address=contract_address_1, abi=abi)
contract2 = w3.eth.contract(address=contract_address_2, abi=abi)

def get_raw_tx(contract, name):
    print(f"Fetching data from {name}...")
    try:
        data = contract.functions.getAll().call()
        print(f"Got {len(data)} bytes from {name}")
        return data
    except Exception as e:
        print(f"Error fetching data from {name}: {e}")
        return None

raw_tx1 = get_raw_tx(contract1, "Contract 1")
raw_tx2 = get_raw_tx(contract2, "Contract 2")

if not raw_tx1 or not raw_tx2:
    print("Failed to fetch data")
    exit(1)

# Decode RLP
def decode_tx(raw_tx):
    # Check for EIP-2718 typed transaction
    if raw_tx[0] <= 0x7f:
        tx_type = raw_tx[0]
        payload = raw_tx[1:]
        decoded = rlp.decode(payload)
        return tx_type, decoded
    else:
        # Legacy transaction
        decoded = rlp.decode(raw_tx)
        return 0, decoded

type1, decoded1 = decode_tx(raw_tx1)
type2, decoded2 = decode_tx(raw_tx2)

print(f"Tx1 Type: {type1}")
print(f"Tx2 Type: {type2}")

# Extract r, s, v and message hash
# Legacy: [nonce, gasPrice, gasLimit, to, value, data, v, r, s]
# EIP-1559: [chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, destination, amount, data, access_list, signature_y_parity, signature_r, signature_s]

def extract_sig_and_msg(tx_type, decoded, raw_tx):
    if tx_type == 0: # Legacy
        nonce, gasPrice, gasLimit, to, value, data, v, r, s = decoded
        # To get the message hash, we need to re-encode the tx without signature
        # EIP-155: rlp([nonce, gasPrice, gasLimit, to, value, data, chainId, 0, 0])
        # But we need to check if v includes chainId.
        # v = chainId * 2 + 35 or v = chainId * 2 + 36
        v_int = int.from_bytes(v, 'big') if isinstance(v, bytes) else v
        r_int = int.from_bytes(r, 'big') if isinstance(r, bytes) else r
        s_int = int.from_bytes(s, 'big') if isinstance(s, bytes) else s

        if v_int >= 35:
            chain_id = (v_int - 35) // 2
            recovery_id = v_int - (chain_id * 2 + 35)
            # Re-encode for signing
            # For legacy with chainId, we append chainId, 0, 0
            tx_to_hash = [nonce, gasPrice, gasLimit, to, value, data, chain_id, 0, 0]
        else:
            # Pre EIP-155
            recovery_id = v_int - 27
            tx_to_hash = [nonce, gasPrice, gasLimit, to, value, data]

        encoded_tx = rlp.encode(tx_to_hash)
        msg_hash = keccak(encoded_tx)
        return r_int, s_int, recovery_id, msg_hash, chain_id if v_int >= 35 else None

    elif tx_type == 2: # EIP-1559
        # [chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, destination, amount, data, access_list, signature_y_parity, signature_r, signature_s]
        chain_id, nonce, max_prio, max_fee, gas_limit, to, value, data, access_list, y_parity, r, s = decoded

        # Structure for signing: 0x02 || rlp([chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, destination, amount, data, access_list])
        tx_to_hash = [chain_id, nonce, max_prio, max_fee, gas_limit, to, value, data, access_list]
        encoded_payload = rlp.encode(tx_to_hash)
        encoded_tx = bytes([tx_type]) + encoded_payload
        msg_hash = keccak(encoded_tx)

        r_int = int.from_bytes(r, 'big') if isinstance(r, bytes) else r
        s_int = int.from_bytes(s, 'big') if isinstance(s, bytes) else s
        v_int = int.from_bytes(y_parity, 'big') if isinstance(y_parity, bytes) else y_parity # 0 or 1

        return r_int, s_int, v_int, msg_hash, chain_id
    else:
        print(f"Unsupported tx type {tx_type}")
        return None

sig1 = extract_sig_and_msg(type1, decoded1, raw_tx1)
sig2 = extract_sig_and_msg(type2, decoded2, raw_tx2)

if not sig1 or not sig2:
    print("Failed to extract signatures")
    exit(1)

r1, s1, v1, z1_bytes, cid1 = sig1
r2, s2, v2, z2_bytes, cid2 = sig2

z1 = int.from_bytes(z1_bytes, 'big')
z2 = int.from_bytes(z2_bytes, 'big')

print(f"r1: {hex(r1)}")
print(f"s1: {hex(s1)}")
print(f"z1: {hex(z1)}")

print(f"r2: {hex(r2)}")
print(f"s2: {hex(s2)}")
print(f"z2: {hex(z2)}")

if r1 == r2:
    print("r values match! Possible nonce reuse.")
    # k = (z1 - z2) * (s1 - s2)^-1 mod n
    # d = (s1 * k - z1) * r^-1 mod n

    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141 # secp256k1 order

    diff_s = (s1 - s2) % n
    diff_z = (z1 - z2) % n

    # Modular inverse
    inv_diff_s = pow(diff_s, -1, n)

    k = (diff_z * inv_diff_s) % n

    inv_r = pow(r1, -1, n)
    d = (inv_r * (s1 * k - z1)) % n

    print(f"Recovered private key: {hex(d)}")
    print(f"Flag: r00t{{0x{hex(d)[2:]}}}")

    # Verify address
    account = Account.from_key(hex(d))
    print(f"Address: {account.address}")

    # Double check signature recovery
    # We can try to recover the public key from the message hash and signature using eth_account
    # However, recovering d is enough.

else:
    print("r values do not match.")
