import time
from web3 import Web3
from colorama import Fore, Style, init
from tqdm import tqdm
from config import ADDRESS_1, PRIVATE_KEY_1, ADDRESS_2, PRIVATE_KEY_2, ALCHEMY_URL

# Initialize colorama for colorful terminal outputs
init(autoreset=True)

# Web3 setup for Base network
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
if not w3.is_connected():
    raise Exception(Fore.RED + "Error: Unable to connect to Base network!")

# Ensure the addresses are in checksum format
ADDRESS_1 = w3.to_checksum_address(ADDRESS_1)
ADDRESS_2 = w3.to_checksum_address(ADDRESS_2)

# Gas price fetching function (Optional - Depending on whether Base has its own gas API)
def get_current_gas_price():
    # Base network should use standard Ethereum gas price fetching methods
    try:
        gas_price = w3.eth.gas_price
        print(Fore.CYAN + f"Gas price fetched: {gas_price} Wei")
        return gas_price
    except Exception as e:
        print(Fore.YELLOW + f"Warning: Gas price fetch failed ({e}). Using fallback gas price.")
        return w3.eth.gas_price

# Token transfer logic (Unchanged)
def get_token_contract(token_address):
    token_address = w3.to_checksum_address(token_address)
    TOKEN_ABI = [
        {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
        {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"},
        {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    ]
    return w3.eth.contract(address=token_address, abi=TOKEN_ABI)

def get_balance(address, token_address):
    address = w3.to_checksum_address(address)
    token_contract = get_token_contract(token_address)
    balance = token_contract.functions.balanceOf(address).call()
    decimals = token_contract.functions.decimals().call()
    formatted_balance = balance / (10 ** decimals)
    print(Fore.GREEN + f"Balance of {address}: {formatted_balance:.6f}")
    return formatted_balance

def transfer_token(sender_private_key, sender_address, token_address, receiver_address, amount):
    sender_address = w3.to_checksum_address(sender_address)
    receiver_address = w3.to_checksum_address(receiver_address)

    token_contract = get_token_contract(token_address)
    decimals = token_contract.functions.decimals().call()
    amount_in_wei = int(amount * (10 ** decimals))
    gas_price = get_current_gas_price()

    nonce = w3.eth.get_transaction_count(sender_address)
    tx = {
        "nonce": nonce,
        "gasPrice": gas_price,
        "gas": 100000,
        "to": token_address,
        "value": 0,
        "data": token_contract.functions.transfer(receiver_address, amount_in_wei).build_transaction({"from": sender_address})["data"],
    }
    signed_tx = w3.eth.account.sign_transaction(tx, sender_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(Fore.GREEN + f"Transaction sent! Hash: {w3.to_hex(tx_hash)}")
    return tx_hash

# Main bot logic with wallet switching (Unchanged)
def alternate_transfers(token_addresses, amount, times, delay_seconds, sleep_time_minutes):
    address_1, private_key_1 = ADDRESS_1, PRIVATE_KEY_1
    address_2, private_key_2 = ADDRESS_2, PRIVATE_KEY_2

    print(Style.BRIGHT + Fore.MAGENTA + "\n--- Alternating Transfers Bot ---")
    print(Fore.YELLOW + f"Initiating {times} transfers with a {delay_seconds}-second delay...\n")

    for i in tqdm(range(1, times + 1), desc="Processing Transfers"):
        balances = {}
        for token_address in token_addresses:
            balances[token_address] = {
                'balance_1': get_balance(address_1, token_address),
                'balance_2': get_balance(address_2, token_address)
            }

        # Determine which wallet to use based on available balance
        if i % 2 == 1 and balances[token_addresses[0]]['balance_1'] >= amount:
            sender, private_key, receiver = address_1, private_key_1, address_2
        elif i % 2 == 0 and balances[token_addresses[0]]['balance_2'] >= amount:
            sender, private_key, receiver = address_2, private_key_2, address_1
        elif balances[token_addresses[0]]['balance_1'] >= amount:  # Switch to address 1 if address 2 is out of balance
            print(Fore.CYAN + f"Switching to Address 1 for Transaction {i}")
            sender, private_key, receiver = address_1, private_key_1, address_2
        elif balances[token_addresses[0]]['balance_2'] >= amount:  # Switch to address 2 if address 1 is out of balance
            print(Fore.CYAN + f"Switching to Address 2 for Transaction {i}")
            sender, private_key, receiver = address_2, private_key_2, address_1
        else:
            print(Fore.RED + "Error: Both wallets have insufficient balance! Terminating process.")
            break

        print(Fore.BLUE + f"\nTransaction {i} in progress...")
        try:
            tx_hash = transfer_token(private_key, sender, token_addresses[0], receiver, amount)
            print(Fore.GREEN + f"Transaction {i} successful! Hash: {tx_hash.hex()}")
        except Exception as e:
            print(Fore.RED + f"Transaction {i} failed: {e}")
            break

        if i < times:
            print(Fore.CYAN + f"Waiting {delay_seconds} seconds for the next transaction...")
            time.sleep(delay_seconds)

    print(Style.BRIGHT + Fore.MAGENTA + "\n--- All Transfers Completed ---")

    # Sleep for the user-specified duration before starting next round
    sleep_time_seconds = sleep_time_minutes * 60  # Convert minutes to seconds
    print(Fore.CYAN + f"Bot will sleep for {sleep_time_minutes} minutes before starting the next round.")
    time.sleep(sleep_time_seconds)

    # Optionally, continue running after sleep
    print(Fore.YELLOW + "Starting new round of transfers...")
    alternate_transfers(token_addresses, amount, times, delay_seconds, sleep_time_minutes)

if __name__ == "__main__":
    # Ask for token contract addresses
    print(Style.BRIGHT + Fore.CYAN + "Welcome to the Ethereum Token Transfer Bot!")
    token_address_1 = input(Fore.YELLOW + "Enter the first token contract address: ").strip()
    token_address_2 = input(Fore.YELLOW + "Enter the second token contract address (optional): ").strip()
    token_address_3 = input(Fore.YELLOW + "Enter the third token contract address (optional): ").strip()

    # Ask for the sleep time before the first transfer cycle starts
    sleep_time_minutes = int(input(Fore.YELLOW + "Enter the time to sleep (in minutes) before starting the transfer cycle: ").strip())

    # Make sure the token addresses are valid (allow optional addresses)
    token_addresses = [w3.to_checksum_address(token_address_1)]
    if token_address_2:
        token_addresses.append(w3.to_checksum_address(token_address_2))
    if token_address_3:
        token_addresses.append(w3.to_checksum_address(token_address_3))

    amount = float(input(Fore.YELLOW + "Enter the amount to send per transfer: ").strip())
    times = int(input(Fore.YELLOW + "Enter the number of transfers: ").strip())
    delay_seconds = int(input(Fore.YELLOW + "Enter the delay between transfers (seconds): ").strip())

    # Start the first transfer cycle
    alternate_transfers(token_addresses, amount, times, delay_seconds, sleep_time_minutes)
