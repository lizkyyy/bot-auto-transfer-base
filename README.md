Setup Instructions

1. Clone the Repository

First, clone the repository to your local machine:

git clone https://github.com/yourusername/token-transfer-bot.git
cd token-transfer-bot

2. Install Dependencies

Install the required libraries using pip:

pip install -r requirements.txt

3. Get Your Alchemy API Key

Go to Alchemy and sign up.

Create a new application for the Base Network and copy the API URL.


4. Get a BaseScan API Key (Optional)

For fetching gas prices, you can use the BaseScan API:

Go to BaseScan and get an API key.


Configuration

1. Edit config.py

In the config.py file, update the following variables with your own details:

ALCHEMY_URL = "https://base-alchemy-api-url"  # Replace with your Alchemy API URL
ADDRESS_1 = "0xYourFirstAddress"              # Replace with your first wallet address
PRIVATE_KEY_1 = "YourPrivateKey1"            # Replace with your first wallet's private key
ADDRESS_2 = "0xYourSecondAddress"            # Replace with your second wallet address
PRIVATE_KEY_2 = "YourPrivateKey2"            # Replace with your second wallet's private key

2. Edit main.py

You can add token contract addresses in main.py when prompted. When the bot runs, it will ask for these values.

3. Token Contract Addresses

When the bot asks for the token contract address, provide the ERC-20 token address you want to transfer.

Running the Bot

Once everything is configured, you can start the bot by running:

python main.py

This bot will alternate between two wallets and transfer ERC-20 tokens on the Base Network.

Configuration Options in main.py

The bot will ask the following:

Token contract addresses: Enter up to three token addresses.

Sleep time (in minutes): Time to wait before starting the transfer cycle.

Amount to send per transfer: Specify how much token to transfer each time.

Number of transfers: Specify how many transfers the bot should execute.

Delay between transfers (seconds): How long to wait between each transfer.


Troubleshooting

Make sure the Alchemy URL is for the Base Network and not Ethereum.

Check that your wallet addresses have enough tokens for transfer and enough ETH (or equivalent) for gas fees.

Ensure your BaseScan API key is correct for gas price fetching.
