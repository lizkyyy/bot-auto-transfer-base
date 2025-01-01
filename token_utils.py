import requests
from web3 import Web3
from config import ALCHEMY_URL

# Initialize Web3 connection
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

if not w3.is_connected():
    raise Exception("Unable to connect to Base network")

def get_current_gas_price():
    """
    Fetches the current gas price from BaseScan with fallback to Web3's default gas price.
    """
    BASESCAN_API_KEY = "YOUR_BASESCAN_API_KEY"  # Replace with your actual BaseScan API key
    url = f'https://api.basescan.org/api?module=gastracker&action=gasoracle&apikey={BASESCAN_API_KEY}'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == '1' and 'result' in data:
                gas_price_gwei = data['result'].get('FastGasPrice')
                if gas_price_gwei:
                    # Convert gas price from Gwei to Wei and return it
                    print(f"Fetched gas price: {gas_price_gwei} Gwei")
                    return int(float(gas_price_gwei) * 10**9)  # Convert Gwei to Wei
        print("Error: Unable to fetch gas price from BaseScan. Using fallback gas price.")
    except Exception as e:
        print(f"Error fetching gas price: {e}. Using fallback gas price.")

    # Fallback gas price using Web3's default
    fallback_price = w3.eth.gas_price
    print(f"Fallback gas price: {fallback_price} Wei")
    return fallback_price

def get_token_contract(token_address):
    """
    Returns a token contract object for interacting with the Base network.
    """
    # Ensure token address is in checksum format
    token_address = Web3.to_checksum_address(token_address)
    
    TOKEN_ABI = [
        {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
        {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"},
        {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    ]
    return w3.eth.contract(address=token_address, abi=TOKEN_ABI)

def get_balance(address, token_address):
    """
    Retrieves the token balance of an address on the Base network.
    """
    # Ensure address is in checksum format
    address = Web3.to_checksum_address(address)
    
    token_contract = get_token_contract(token_address)
    balance = token_contract.functions.balanceOf(address).call()
    decimals = token_contract.functions.decimals().call()
    formatted_balance = balance / (10 ** decimals)
    print(f"Balance of {address}: {formatted_balance}")
    return formatted_balance

def transfer_token(sender_private_key, sender_address, token_address, receiver_address, amount):
    """
    Executes a token transfer on the Base network with dynamic gas price.
    """
    # Ensure all addresses are in checksum format
    sender_address = Web3.to_checksum_address(sender_address)
    receiver_address = Web3.to_checksum_address(receiver_address)
    token_address = Web3.to_checksum_address(token_address)

    token_contract = get_token_contract(token_address)

    # Convert amount to the smallest unit
    decimals = token_contract.functions.decimals().call()
    amount_in_wei = int(amount * (10 ** decimals))

    # Fetch and adjust gas price
    gas_price = get_current_gas_price()
    adjusted_gas_price = int(gas_price * 1.1)  # Add a 10% buffer for priority (optional)

    # Get the current nonce
    nonce = w3.eth.get_transaction_count(sender_address)

    # Build the transaction
    tx = {
        "nonce": nonce,
        "gasPrice": adjusted_gas_price,  # Use the gas price fetched in Wei
        "gas": 100000,  # You might want to estimate gas more dynamically
        "to": token_address,
        "value": 0,
        "data": token_contract.functions.transfer(receiver_address, amount_in_wei).build_transaction({"from": sender_address})["data"],
    }

    try:
        # Sign the transaction
        signed_tx = w3.eth.account.sign_transaction(tx, sender_private_key)

        # Send the transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction sent! Hash: {w3.to_hex(tx_hash)}")
        return tx_hash
    except Exception as e:
        print(f"Error sending transaction: {e}")
        raise
