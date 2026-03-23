import tkinter as tk
from web3 import Web3

# ================== CONFIG ==================
INFURA_URL = "https://sepolia.infura.io/v3/11111111111111111111111111111111"

# Use a valid-format dummy address (so no error)
CONTRACT_ADDRESS = "0x1111111111111111111111111111111111111111"

WALLET_ADDRESS = "0x2222222222222222222222222222222222222222"
PRIVATE_KEY = "0xabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd"
# ===========================================

# Connect to blockchain
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Check connection
connected = w3.is_connected()

# Safely convert address
try:
    contract_address = w3.to_checksum_address(CONTRACT_ADDRESS)
    contract_valid = True
except:
    contract_valid = False

# ABI
ABI = [
    {"inputs": [], "name": "deposit", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [{"internalType": "uint256","name": "amount","type": "uint256"}],
     "name": "withdraw","outputs": [],"stateMutability": "nonpayable","type": "function"},
    {"inputs": [],"name": "getBalance",
     "outputs": [{"internalType": "uint256","name": "","type": "uint256"}],
     "stateMutability": "view","type": "function"}
]

# Create contract only if valid
if contract_valid:
    contract = w3.eth.contract(address=contract_address, abi=ABI)
else:
    contract = None

# ---------------- FUNCTIONS ----------------

def show_network():
    if connected:
        network_label.config(text="🌐 Connected to Sepolia Testnet ✅")
    else:
        network_label.config(text="⚠️ Running in Demo Mode")

def wallet_balance():
    if connected:
        try:
            bal = w3.eth.get_balance(WALLET_ADDRESS)
            eth = w3.from_wei(bal, 'ether')
            result_label.config(text=f"💰 Wallet Balance: {eth} ETH")
        except:
            result_label.config(text="❌ Error fetching balance")
    else:
        result_label.config(text="💰 Demo Balance: 2.5 ETH")

def gas_price():
    if connected:
        try:
            gas = w3.eth.gas_price
            gwei = w3.from_wei(gas, 'gwei')
            result_label.config(text=f"⛽ Gas Price: {gwei} Gwei")
        except:
            result_label.config(text="❌ Error fetching gas price")
    else:
        result_label.config(text="⛽ Demo Gas Price: 15 Gwei")

def deposit():
    if connected and contract:
        try:
            amount = float(amount_entry.get())
            wei = w3.to_wei(amount, 'ether')

            txn = contract.functions.deposit().build_transaction({
                'from': WALLET_ADDRESS,
                'value': wei,
                'nonce': w3.eth.get_transaction_count(WALLET_ADDRESS),
                'gas': 200000,
                'gasPrice': w3.to_wei('10', 'gwei')
            })

            signed = w3.eth.account.sign_transaction(txn, PRIVATE_KEY)
            tx = w3.eth.send_raw_transaction(signed.rawTransaction)

            result_label.config(text=f"⏳ TX Sent\n{tx.hex()}")

        except Exception as e:
            result_label.config(text=f"❌ {e}")
    else:
        result_label.config(text="✅ Demo Deposit Successful")

def withdraw():
    if connected and contract:
        try:
            amount = float(amount_entry.get())
            wei = w3.to_wei(amount, 'ether')

            txn = contract.functions.withdraw(wei).build_transaction({
                'from': WALLET_ADDRESS,
                'nonce': w3.eth.get_transaction_count(WALLET_ADDRESS),
                'gas': 200000,
                'gasPrice': w3.to_wei('10', 'gwei')
            })

            signed = w3.eth.account.sign_transaction(txn, PRIVATE_KEY)
            tx = w3.eth.send_raw_transaction(signed.rawTransaction)

            result_label.config(text=f"⏳ TX Sent\n{tx.hex()}")

        except Exception as e:
            result_label.config(text=f"❌ {e}")
    else:
        result_label.config(text="✅ Demo Withdraw Successful")

def check_balance():
    if connected and contract:
        try:
            bal = contract.functions.getBalance().call({'from': WALLET_ADDRESS})
            eth = w3.from_wei(bal, 'ether')
            result_label.config(text=f"📊 Contract Balance: {eth} ETH")
        except:
            result_label.config(text="❌ Error reading contract")
    else:
        result_label.config(text="📊 Demo Contract Balance: 1.5 ETH")

# ---------------- UI ----------------

root = tk.Tk()
root.title("DeFi Testnet App")
root.geometry("400x400")

tk.Label(root, text="DeFi Dashboard", font=("Arial", 16)).pack(pady=10)

network_label = tk.Label(root, text="")
network_label.pack()
show_network()

tk.Button(root, text="Wallet Balance", command=wallet_balance).pack(pady=5)
tk.Button(root, text="Gas Price", command=gas_price).pack(pady=5)

tk.Label(root, text="Enter Amount (ETH)").pack()
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

tk.Button(root, text="Deposit", command=deposit, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="Withdraw", command=withdraw, bg="red", fg="white").pack(pady=5)
tk.Button(root, text="Contract Balance", command=check_balance).pack(pady=5)

result_label = tk.Label(root, text="", wraplength=350)
result_label.pack(pady=10)

root.mainloop()