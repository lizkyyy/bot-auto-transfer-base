from web3 import Web3
from config import ALCHEMY_URL
from main import get_current_gas_price  # Import the updated gas price fetching function

# Initialize Web3 connection for Base Network
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

def get_token_contract(token_address):
    """
    Returns a token contract object for interacting with the token on Base network.
    """
    token_address = Web3.to_checksum_address(token_address)
    TOKEN_ABI = [
        {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
        {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"},
        {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    ]
    return w3.eth.contract(address=token_address, abi=TOKEN_ABI)

def get_balance(address, token_address):
    """
    Retrieves the token balance of an address on Base network.
    """
    address = w3.to_checksum_address(address)
    token_contract = get_token_contract(token_address)
    balance = token_contract.functions.balanceOf(address).call()
    decimals = token_contract.functions.decimals().call()
    formatted_balance = balance / (10 ** decimals)
    print(f"Balance of {address}: {formatted_balance}")
    return formatted_balance

def transfer_token(sender_private_key, sender_address, token_address, receiver_address, amount):
    """
    Executes a token transfer with dynamic gas price from BaseScan for Base network.
    """
    sender_address = Web3.to_checksum_address(sender_address)
    receiver_address = Web3.to_checksum_address(receiver_address)
    token_address = Web3.to_checksum_address(token_address)

    token_contract = get_token_contract(token_address)
    decimals = token_contract.functions.decimals().call()
    amount_in_wei = int(amount * (10 ** decimals))

    # Fetch gas price using the new BaseScan integration
    gas_price = get_current_gas_price()  # Fetch from BaseScan or fallback
    adjusted_gas_price = int(gas_price * 1.1)  # Add buffer (optional)

    # Get nonce for transaction
    nonce = w3.eth.get_transaction_count(sender_address)

    # Build the transaction object
    tx = {
        "nonce": nonce,
        "gasPrice": adjusted_gas_price,
        "gas": 100000,  # You might want to estimate gas dynamically
        "to": token_address,
        "value": 0,
        "data": token_contract.functions.transfer(receiver_address, amount_in_wei).build_transaction({"from": sender_address})["data"],
    }

    try:
        # Sign and send the transaction
        signed_tx = w3.eth.account.sign_transaction(tx, sender_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction sent! Hash: {w3.to_hex(tx_hash)}")
        return tx_hash
    except Exception as e:
        print(f"Error sending transaction: {e}")
        raise
