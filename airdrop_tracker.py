import requests
import json
import time

ETHERSCAN_API_KEY = "YourApiKeyToken"
ADDRESS_TO_SCAN = None  # будет введён пользователем
TX_COUNT = 50

# Список адресов известных дроперов (заполняется вручную)
KNOWN_AIRDROP_SENDERS = {
    "0x111111111111111111111111111111111111dead": "Example Airdropper",
    "0x222222222222222222222222222222222222feed": "Testnet Faucet",
    # Добавь свои адреса сюда
}

def fetch_transactions(address):
    url = (
        f"https://api.etherscan.io/api"
        f"?module=account&action=txlist"
        f"&address={address}"
        f"&startblock=0&endblock=99999999"
        f"&sort=desc"
        f"&apikey={ETHERSCAN_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    if data["status"] != "1":
        print("⚠️  API error:", data.get("message"))
        return []
    return data["result"][:TX_COUNT]

def find_airdrop_sources(transactions):
    print(f"\n🔎 Scanning for known airdrop senders in last {TX_COUNT} transactions...\n")
    found = False
    for tx in transactions:
        sender = tx["from"].lower()
        if sender in KNOWN_AIRDROP_SENDERS:
            name = KNOWN_AIRDROP_SENDERS[sender]
            amount = int(tx["value"]) / 1e18
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(tx["timeStamp"])))
            print(f"🎁 Airdrop match found!")
            print(f"   From: {sender} ({name})")
            print(f"   Amount: {amount:.6f} ETH")
            print(f"   Time: {timestamp}")
            print(f"   TxHash: {tx['hash']}\n")
            found = True
    if not found:
        print("No known airdrop senders found.")

def main():
    global ADDRESS_TO_SCAN
    address = input("Enter wallet address to scan: ").strip()
    if not address.startswith("0x") or len(address) != 42:
        print("❌ Invalid Ethereum address.")
        return

    ADDRESS_TO_SCAN = address
    txs = fetch_transactions(ADDRESS_TO_SCAN)
    if txs:
        find_airdrop_sources(txs)
    else:
        print("No transactions found.")

if __name__ == "__main__":
    main()
