import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
BASE_URL = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"

wallet_address = "0x3f5CE5FBFe3E9af3971dD833D26BA9b5C936f0bE" # Carteira de exemplo, estamos usando a Binance Hot Wallet para testes

headers = {"Content-Type": "application/json"}

def get_latest_transfers(address):
    url = BASE_URL
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "alchemy_getAssetTransfers",
        "params": [{
            "fromBlock": "0x0",
            "toAddress": address,
            "category": ["external", "erc20", "erc721"],
            "excludeZeroValue": True,
            "maxCount": "0xA"  # 10
        }]
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print('[ERRO] Código HTTP:', response.status_code)
        print('[ERRO] Resposta:', response.text)
        return []

    try:
        result = response.json().get("result", {})
        return result.get("transfers", [])
    except Exception as e:
        print('[ERRO] Falha ao converter resposta JSON:', e)
        print('[ERRO] Conteúdo bruto:', response.text)
        return []

print(f'[+] Iniciando monitoramento da carteira: {wallet_address}')
last_hash = None

while True:
    txs = get_latest_transfers(wallet_address)
    if txs:
        latest = txs[0]
        if latest['hash'] != last_hash:
            print('\n[!!!] Nova transação detectada:')
            print(f'    Hash: {latest["hash"]}')
            print(f'    Token: {latest.get("asset", "ETH")}')
            print(f'    Valor: {latest.get("value", "N/A")}')
            print(f'    De: {latest["from"]} -> Para: {latest["to"]}')
            print(f'    Timestamp: {latest.get("metadata", {}).get("blockTimestamp", "desconhecido")}')
            last_hash = latest["hash"]
    time.sleep(10)
