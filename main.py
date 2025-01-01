from config import ALCHEMY_URL, ADDRESS_1, PRIVATE_KEY_1, ADDRESS_2
from token_utils import get_balance, transfer_token

def main():
    # Check balance of ADDRESS_1 on Base network
    token_address = "0xYourTokenAddressHere"  # Replace with your token address on Base
    print("Checking balance for ADDRESS_1:")
    balance = get_balance(ADDRESS_1, token_address)
    print(f"Balance of ADDRESS_1: {balance} tokens")
    
    # Transfer tokens from ADDRESS_1 to ADDRESS_2
    amount_to_transfer = 10  # Replace with the amount you want to transfer
    print(f"Transferring {amount_to_transfer} tokens from ADDRESS_1 to ADDRESS_2.")
    
    # Call the transfer function
    transfer_token(PRIVATE_KEY_1, ADDRESS_1, token_address, ADDRESS_2, amount_to_transfer)

if __name__ == "__main__":
    main()
