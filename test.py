#take an input of contract address and give option to control the master admin of the contract, and also give option to see the live status of the contract

from web3 import Web3
import json

# Connect to the blockchain
rpc_url = input("Enter the RPC URL of your blockchain: ")
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Check if the connection is successful
if web3.is_connected():
    print("Connected to the blockchain successfully!")

    # Ask for role
    role = input("Are you admin or user? ").lower().strip()

    if role == 'user':
        # User menu
        while True:
            print("\nUser Options:")
            print("1. View balance of an address")
            print("2. View live status of all accounts")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                address = input("Enter the address to check the balance: ")
                address = Web3.to_checksum_address(address)
                balance = web3.eth.get_balance(address)
                print(f"The balance of the address {address} is: {web3.from_wei(balance, 'ether')} Ether")
            elif choice == '2':
                print("\nLive status of all accounts:")
                accounts = web3.eth.accounts
                for acc in accounts:
                    bal = web3.eth.get_balance(acc)
                    print(f"{acc}: {web3.from_wei(bal, 'ether')} Ether")
            elif choice == '3':
                break
            else:
                print("Invalid choice")

    elif role == 'admin':
        # Admin menu, includes contract interactions
        # Contract interaction
        contract_address = input("\nEnter the contract address: ")
        contract_address = Web3.to_checksum_address(contract_address)

        # Check if contract is deployed
        code = web3.eth.get_code(contract_address)
        if code == '0x':
            print("No contract found at this address. Please check the address or deploy a new contract.")
        else:

            # Assume ABI for a token contract with owner, transferOwnership, mint, transfer, balanceOf, name, symbol, decimals, totalSupply, burn
            abi = [
            {
                "inputs": [],
                "name": "owner",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}],
                "name": "transferOwnership",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}],
                "name": "mint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "name",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]

            contract = web3.eth.contract(address=contract_address, abi=abi)

            while True:
                print("\nAdmin Options:")
                print("1. View balance of an address")
                print("2. View live status of all accounts")
                print("3. See live status of the contract (current admin)")
                print("4. Control master admin (transfer ownership)")
                print("5. Mint tokens")
                print("6. Burn tokens")
                print("7. Transfer tokens")
                print("8. Send ETH to address")
                print("9. View token balance of an address")
                print("10. View past token transfers")
                print("11. Deploy a new contract")
                print("12. View contract information")
                print("13. Exit")
                choice = input("Enter your choice: ")
                if choice == '1':
                    address = input("Enter the address to check the balance: ")
                    address = Web3.to_checksum_address(address)
                    balance = web3.eth.get_balance(address)
                    print(f"The balance of the address {address} is: {web3.from_wei(balance, 'ether')} Ether")
                elif choice == '2':
                    print("\nLive status of all accounts:")
                    accounts = web3.eth.accounts
                    for acc in accounts:
                        bal = web3.eth.get_balance(acc)
                        print(f"{acc}: {web3.from_wei(bal, 'ether')} Ether")
                elif choice == '3':
                    try:
                        owner = contract.functions.owner().call()
                        print(f"Current admin: {owner}")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == '4':
                    new_admin = input("Enter new admin address: ")
                    new_admin = Web3.to_checksum_address(new_admin)
                    try:
                        tx = contract.functions.transferOwnership(new_admin).transact({'from': web3.eth.accounts[0], 'gas': 2000000})
                        receipt = web3.eth.wait_for_transaction_receipt(tx)
                        if receipt['status'] == 1:
                            print("Ownership transferred successfully.")
                        else:
                            print("Transaction failed.")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == '5':
                    to = input("Enter recipient address: ")
                    to = Web3.to_checksum_address(to)
                    amount = int(input("Enter amount to mint: "))
                    try:
                        tx = contract.functions.mint(to, amount).transact({'from': web3.eth.accounts[0], 'gas': 2000000})
                        receipt = web3.eth.wait_for_transaction_receipt(tx)
                        if receipt['status'] == 1:
                            print("Tokens minted successfully.")
                        else:
                            print("Transaction failed.")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == '6':
                    amount = int(input("Enter amount to burn: "))
                    try:
                        tx = contract.functions.burn(amount).transact({'from': web3.eth.accounts[0], 'gas': 2000000})
                        receipt = web3.eth.wait_for_transaction_receipt(tx)
                        if receipt['status'] == 1:
                            print("Tokens burned successfully.")
                        else:
                            print("Transaction failed.")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == '7':
                    to = input("Enter recipient address: ")
                    to = Web3.to_checksum_address(to)
                    amount = int(input("Enter amount to transfer: "))
                    try:
                        tx = contract.functions.transfer(to, amount).transact({'from': web3.eth.accounts[0], 'gas': 2000000})
                        receipt = web3.eth.wait_for_transaction_receipt(tx)
                        if receipt['status'] == 1:
                            print("Tokens transferred successfully.")
                        else:
                            print("Transaction failed.")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == '8':
                    to = input("Enter recipient address: ")
                    to = Web3.to_checksum_address(to)
                    amount_wei = web3.to_wei(input("Enter amount in ETH: "), 'ether')
                    try:
                        tx = web3.eth.send_transaction({'from': web3.eth.accounts[0], 'to': to, 'value': amount_wei, 'gas': 21000})
                        receipt = web3.eth.wait_for_transaction_receipt(tx)
                        if receipt['status'] == 1:
                            print("ETH sent successfully.")
                        else:
                            print("Transaction failed.")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == '9':
                    address = input("Enter address to check token balance: ")
                    address = Web3.to_checksum_address(address)
                    try:
                        balance = contract.functions.balanceOf(address).call()
                        print(f"Token balance of {address}: {balance}")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == '10':
                    try:
                        events = contract.events.Transfer.get_logs(fromBlock=0)
                        if events:
                            print("Past token transfers:")
                            for event in events:
                                print(f"From: {event.args['from']}, To: {event.args['to']}, Value: {event.args['value']}")
                        else:
                            print("No transfers found.")
                    except Exception as e:
                        print(f"Error retrieving transfers: {e}")
                elif choice == '11':
                    # Deploy contract
                    contract_source = '''
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract HuntCoin is ERC20 {
    address public owner;

    constructor(address _owner) ERC20("Hunt Coin", "thc") {
        owner = _owner;
        _mint(owner, 1000000 * 10 ** decimals());
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    function burn(uint256 amount) public onlyOwner {
        _burn(owner, amount);
    }
}
'''
                    try:
                        from solcx import compile_source
                        compiled_sol = compile_source(contract_source, import_remappings=['@openzeppelin/=c:/Users/VICTUS/Desktop/blockchain_final/.deps/npm/@openzeppelin/'])
                        contract_interface = compiled_sol['<stdin>:HuntCoin']
                        contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bytecode'])
                        tx = contract.constructor(web3.eth.accounts[0]).transact({'from': web3.eth.accounts[0], 'gas': 3000000})
                        receipt = web3.eth.wait_for_transaction_receipt(tx)
                        if receipt['status'] == 1:
                            deployed_address = receipt['contractAddress']
                            print(f"Contract deployed at: {deployed_address}")
                            # Save ABI and address
                            with open('contract_config.json', 'w') as f:
                                json.dump({'address': deployed_address, 'abi': contract_interface['abi']}, f)
                            print("Config saved to contract_config.json")
                        else:
                            print("Deployment failed.")
                    except ImportError:
                        print("solcx not installed. Install with pip install py-solc-x")
                    except Exception as e:
                        print(f"Error: {e}")
                elif choice == '12':
                    print(f"Contract Address: {contract_address}")
                    print("ABI:")
                    print(json.dumps(abi, indent=2))
                    try:
                        name = contract.functions.name().call()
                        symbol = contract.functions.symbol().call()
                        decimals = contract.functions.decimals().call()
                        total_supply = contract.functions.totalSupply().call()
                        owner = contract.functions.owner().call()
                        print(f"Name: {name}")
                        print(f"Symbol: {symbol}")
                        print(f"Decimals: {decimals}")
                        print(f"Total Supply: {total_supply}")
                        print(f"Owner: {owner}")
                    except Exception as e:
                        print(f"Error retrieving contract details: {e}")
                elif choice == '13':
                    break
                else:
                    print("Invalid choice")
    else:
        print("Invalid role. Please enter 'admin' or 'user'.")
else:
    print("Failed to connect to the blockchain. Please check your RPC URL and try again.") 
