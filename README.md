# Bot Auto Transfer Base

This project is a base template for a bot that automatically transfers tokens between two Ethereum addresses. It supports customizable delays, automatic address switching when one address runs out of tokens, and the ability to specify transfer amounts and token addresses.

## Features

- **Automatic Token Transfer**: Transfers tokens from one address to another.
- **Address Switching**: Automatically switches between addresses when one runs out of tokens.
- **Customizable Delay**: You can set delays between transfers to avoid overloading the network.
- **Configurable Amounts**: Allows you to specify the amount of tokens to transfer in each transaction.
- **Supports Custom Tokens**: You can set the token addresses for ERC-20 token transfers.

## Prerequisites

- Python 3.x
- [Alchemy API Key](https://www.alchemy.com) for interacting with the Ethereum network.
- An Ethereum wallet with funds.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lizkyyy/bot-auto-transfer-base.git

2. Navigate into the project directory:
   ```bash
   cd bot-auto-transfer-base


3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt


4. Add your wallet details and Alchemy API URL in config.py:
   ```bash
   ALCHEMY_URL = "your-alchemy-url"
   ADDRESS_1 = "your-first-wallet-address"
   PRIVATE_KEY_1 = "your-first- wallet-private-key"
   ADDRESS_2 = "your-second-wallet-address"
   PRIVATE_KEY_2 = "your-second-wallet-private-key"

Make sure to replace "your-alchemy-url", "your-first-wallet-address", and the corresponding private keys with the correct values.

Usage

Run the bot script to begin transferring tokens:
   ```bash
   python main.py
