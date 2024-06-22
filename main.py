import os
import sys
import json
import asyncio
from web3 import Web3
from eth_account import Account
from mnemonic import Mnemonic
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
import requests

console = Console()

INFURA_PROJECT_ID = "a8cb0c33a1c44927a2ea6fce2b4ba608"
BSCSCAN_API_KEY = "WHX4VAY9NTK33I5NZHNCGMYBK568CEVMSK"

def show_instructions():
    console.print("[bold green]---EVM Wallet Scanner:---[/bold green]", style="bold")
    console.print("[bold red]Software Developed by Pikai[/bold red]\n")
    console.print("This software scans seed phrases to find associated wallet addresses and their balances on Ethereum, Polygon, and BSC.\n")
    console.print("[bold red]Follow the below Instructions to scan:[/bold red]")
    console.print("1. Prepare a .txt file containing seed phrases (12 or 24 words per line with a single space after each words, up to 500 lines).")
    console.print("2. The software will check these seed phrases against Ethereum, Binance Smart Chain (BSC), and Polygon networks.")
    console.print("3. Results will be displayed and can be exported to a .txt file.\n")

def load_seed_phrases(file_path):
    if not os.path.exists(file_path):
        console.print(f"[bold red]File not found: {file_path}[/bold red]")
        sys.exit(1)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    seed_phrases = [line.strip() for line in lines if line.strip()]
    if len(seed_phrases) > 500:
        console.print("[bold red]The file contains more than 500 lines.[/bold red]")
        sys.exit(1)
    
    return seed_phrases

def validate_seed_phrases(seed_phrases):
    mnemonic = Mnemonic("english")
    valid_phrases = []

    for phrase in seed_phrases:
        if mnemonic.check(phrase):
            valid_phrases.append(phrase)
        else:
            console.print(f"[bold yellow]Invalid seed phrase skipped: {phrase}[/bold yellow]")

    return valid_phrases

def generate_wallets(seed_phrases):
    console.print("Enabling HD wallet features...")
    Account.enable_unaudited_hdwallet_features()  # Enable HD wallet features
    console.print("HD wallet features enabled.")

    wallets = []

    for phrase in seed_phrases:
        console.print(f"Generating wallet for phrase: {phrase}")
        seed = Mnemonic.to_seed(phrase)
        account = Account.from_mnemonic(phrase)
        wallets.append((account.address, phrase))

    return wallets

async def fetch_balance_ethereum(address):
    web3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"))
    balance = web3.eth.get_balance(address)
    return web3.from_wei(balance, 'ether')  # Correct method is from_wei

async def fetch_balance_polygon(address):
    web3 = Web3(Web3.HTTPProvider(f"https://polygon-mainnet.infura.io/v3/{INFURA_PROJECT_ID}"))
    balance = web3.eth.get_balance(address)
    return web3.from_wei(balance, 'ether')  # Correct method is from_wei

async def fetch_balance_bsc(address):
    url = f"https://api.bscscan.com/api"
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "apikey": BSCSCAN_API_KEY
    }
    response = requests.get(url, params=params)
    balance = response.json().get('result')
    return int(balance) / 1e18  # Convert Wei to BNB

async def scan_wallets(wallets):
    results = []

    with Progress() as progress:
        task = progress.add_task("[green]Scanning wallets...", total=len(wallets))

        for address, phrase in wallets:
            eth_balance = await fetch_balance_ethereum(address)
            polygon_balance = await fetch_balance_polygon(address)
            bsc_balance = await fetch_balance_bsc(address)

            results.append({
                "address": address,
                "phrase": phrase,
                "balances": {
                    "ethereum": eth_balance,
                    "polygon": polygon_balance,
                    "bsc": bsc_balance
                }
            })

            progress.advance(task)

    return results

def export_results(results, output_file):
    with open(output_file, 'w') as file:
        for result in results:
            line = f"{result['address']} Ethereum: {result['balances']['ethereum']} BSC: {result['balances']['bsc']} Polygon: {result['balances']['polygon']}\n"
            file.write(line)

    console.print(f"[bold green]Results exported to {output_file}[/bold green]")

def main():
    show_instructions()
    file_path = Prompt.ask("Enter the path to the seed phrases .txt file and press enter")
    seed_phrases = load_seed_phrases(file_path)

    console.print(f"[bold]Loaded {len(seed_phrases)} seed phrases.[/bold]")
    console.print("Validating seed phrases...")

    valid_phrases = validate_seed_phrases(seed_phrases)
    console.print(f"[bold]Found {len(valid_phrases)} valid seed phrases.[/bold]")

    if not valid_phrases:
        console.print("[bold red]No valid seed phrases found. Exiting.[/bold red]")
        sys.exit(1)

    console.print("Generating wallets...")
    wallets = generate_wallets(valid_phrases)

    console.print("Scanning wallets...")
    results = asyncio.run(scan_wallets(wallets))

    console.print("Scan complete.")
    console.print(json.dumps(results, indent=4))

    output_file = Prompt.ask("Enter the output file path to save the results")
    export_results(results, output_file)

if __name__ == "__main__":
    main()
