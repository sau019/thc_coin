from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from web3 import Web3
import json
import os
import hashlib
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Hardcoded ABI from test.py
ABI = [
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

# Database files
USERS_FILE = 'users.json'
PENDING_USERS_FILE = 'pending_users.json'

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)

    # Create default admin user if no users exist
    if not users:
        admin_user = {
            'username': 'admin',
            'password_hash': hash_password('0x5B38Da6a701c568545dCfcB03FcB875f56beddC4'),  # Contract address as password
            'email': 'admin@blockchain.com',
            'full_name': 'System Administrator',
            'address': 'System Address',
            'phone': '000-000-0000',
            'wallet_address': '',
            'created_at': datetime.now().isoformat(),
            'approved_at': datetime.now().isoformat(),
            'role': 'admin'
        }
        users['admin'] = admin_user
        save_users(users)

    return users

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_pending_users():
    if os.path.exists(PENDING_USERS_FILE):
        with open(PENDING_USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_pending_users(pending_users):
    with open(PENDING_USERS_FILE, 'w') as f:
        json.dump(pending_users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_admin():
    return session.get('role') == 'admin'

def is_logged_in():
    return 'username' in session

def get_web3(rpc_url):
    return Web3(Web3.HTTPProvider(rpc_url))

@app.route('/')
def index():
    if is_logged_in():
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))
    pending_users = load_pending_users()
    return render_template('admin.html', pending_users=pending_users)

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json

    # Validate required fields
    required_fields = ['username', 'password', 'email', 'full_name', 'address', 'phone', 'aadhar_number', 'wallet_address']
    for field in required_fields:
        if not data.get(field, '').strip():
            return jsonify({'success': False, 'error': f'{field.replace("_", " ").title()} is required'})

    username = data['username'].strip()
    email = data['email'].strip()
    aadhar_number = data['aadhar_number'].strip()
    wallet_address = data['wallet_address'].strip()

    # Validate Aadhar number (12 digits)
    if not re.match(r'^[0-9]{12}$', aadhar_number):
        return jsonify({'success': False, 'error': 'Aadhar number must be exactly 12 digits'})

    # Validate wallet address format
    if not re.match(r'^0x[a-fA-F0-9]{40}$', wallet_address):
        return jsonify({'success': False, 'error': 'Invalid wallet address format'})

    # Check if user already exists
    users = load_users()
    pending_users = load_pending_users()

    if username in users or username in pending_users:
        return jsonify({'success': False, 'error': 'Username already exists'})

    # Check if email already exists
    for user in users.values():
        if user.get('email') == email:
            return jsonify({'success': False, 'error': 'Email already registered'})

    for user in pending_users.values():
        if user.get('email') == email:
            return jsonify({'success': False, 'error': 'Email already pending approval'})

    # Check if Aadhar number already exists
    for user in users.values():
        if user.get('aadhar_number') == aadhar_number:
            return jsonify({'success': False, 'error': 'Aadhar number already registered'})

    for user in pending_users.values():
        if user.get('aadhar_number') == aadhar_number:
            return jsonify({'success': False, 'error': 'Aadhar number already pending approval'})

    # Create pending user
    pending_user = {
        'username': username,
        'password_hash': hash_password(data['password']),
        'email': email,
        'full_name': data['full_name'].strip(),
        'address': data['address'].strip(),
        'phone': data['phone'].strip(),
        'aadhar_number': aadhar_number,
        'wallet_address': wallet_address,
        'created_at': datetime.now().isoformat(),
        'status': 'pending'
    }

    pending_users[username] = pending_user
    save_pending_users(pending_users)

    return jsonify({'success': True, 'message': 'Registration submitted for admin approval'})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password are required'})

    users = load_users()
    user = users.get(username)

    if not user or user['password_hash'] != hash_password(password):
        return jsonify({'success': False, 'error': 'Invalid credentials'})

    session['username'] = username
    session['role'] = user.get('role', 'user')

    return jsonify({'success': True, 'role': session['role']})

@app.route('/api/admin/approve/<username>', methods=['POST'])
def api_admin_approve(username):
    if not is_logged_in() or not is_admin():
        return jsonify({'success': False, 'error': 'Unauthorized'})

    pending_users = load_pending_users()
    users = load_users()

    if username not in pending_users:
        return jsonify({'success': False, 'error': 'User not found in pending list'})

    # Move user from pending to approved
    user = pending_users.pop(username)
    user['approved_at'] = datetime.now().isoformat()
    user['role'] = 'user'  # Default role

    users[username] = user
    save_users(users)
    save_pending_users(pending_users)

    return jsonify({'success': True, 'message': f'User {username} approved'})

@app.route('/api/admin/reject/<username>', methods=['POST'])
def api_admin_reject(username):
    if not is_logged_in() or not is_admin():
        return jsonify({'success': False, 'error': 'Unauthorized'})

    pending_users = load_pending_users()

    if username not in pending_users:
        return jsonify({'success': False, 'error': 'User not found in pending list'})

    del pending_users[username]
    save_pending_users(pending_users)

    return jsonify({'success': True, 'message': f'User {username} rejected'})

@app.route('/api/admin/pending_users', methods=['POST'])
def api_admin_get_pending_users():
    if not is_logged_in() or not is_admin():
        return jsonify({'success': False, 'error': 'Unauthorized'})

    pending_users = load_pending_users()
    users_list = []
    for username, user_data in pending_users.items():
        users_list.append({
            'username': username,
            'email': user_data.get('email', ''),
            'full_name': user_data.get('full_name', ''),
            'phone': user_data.get('phone', ''),
            'address': user_data.get('address', ''),
            'wallet_address': user_data.get('wallet_address', ''),
            'created_at': user_data.get('created_at', '')
        })

    return jsonify({'success': True, 'users': users_list})

@app.route('/api/admin/approved_users', methods=['POST'])
def api_admin_get_approved_users():
    if not is_logged_in() or not is_admin():
        return jsonify({'success': False, 'error': 'Unauthorized'})

    users = load_users()
    users_list = []
    for username, user_data in users.items():
        if username != 'admin':  # Don't show the default admin in the list
            users_list.append({
                'username': username,
                'email': user_data.get('email', ''),
                'full_name': user_data.get('full_name', ''),
                'role': user_data.get('role', 'user'),
                'approved_at': user_data.get('approved_at', '')
            })

    return jsonify({'success': True, 'users': users_list})

@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')  # Note: test.py uses 7546, but often it's 7545
    web3 = get_web3(rpc_url)
    if web3.is_connected():
        accounts = web3.eth.accounts
        return jsonify({'success': True, 'accounts': accounts})
    else:
        return jsonify({'success': False, 'error': 'Cannot connect to blockchain'})

@app.route('/get_balance', methods=['POST'])
def get_balance():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')
    address = data.get('address', '').strip()

    if not address:
        return jsonify({'error': 'Address is required'})

    try:
        address = Web3.to_checksum_address(address)
    except Exception as e:
        return jsonify({'error': f'Invalid address: {str(e)}'})

    web3 = get_web3(rpc_url)
    if not web3.is_connected():
        return jsonify({'error': 'Cannot connect to blockchain'})

    try:
        balance = web3.eth.get_balance(address)
        return jsonify({'balance': str(web3.from_wei(balance, 'ether'))})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_all_balances', methods=['POST'])
def get_all_balances():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')

    web3 = get_web3(rpc_url)
    if not web3.is_connected():
        return jsonify({'error': 'Cannot connect to blockchain'})

    try:
        accounts = web3.eth.accounts
        balances = {}
        for acc in accounts:
            bal = web3.eth.get_balance(acc)
            balances[acc] = str(web3.from_wei(bal, 'ether'))
        return jsonify(balances)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_contract_owner', methods=['POST'])
def get_contract_owner():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')
    contract_address = data.get('contract_address', '').strip()

    if not contract_address:
        return jsonify({'error': 'Contract address is required'})

    try:
        contract_address = Web3.to_checksum_address(contract_address)
    except Exception as e:
        return jsonify({'error': f'Invalid contract address: {str(e)}'})

    web3 = get_web3(rpc_url)
    if not web3.is_connected():
        return jsonify({'error': 'Cannot connect to blockchain'})

    contract = web3.eth.contract(address=contract_address, abi=ABI)
    try:
        owner = contract.functions.owner().call()
        return jsonify({'owner': owner})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/transfer_ownership', methods=['POST'])
def transfer_ownership():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')
    contract_address = data.get('contract_address', '').strip()
    new_owner = data.get('new_owner', '').strip()
    from_account = data.get('from_account', '')

    if not contract_address:
        return jsonify({'error': 'Contract address is required'})
    if not new_owner:
        return jsonify({'error': 'New owner address is required'})
    if not from_account:
        return jsonify({'error': 'From account is required'})

    try:
        contract_address = Web3.to_checksum_address(contract_address)
        new_owner = Web3.to_checksum_address(new_owner)
        from_account = Web3.to_checksum_address(from_account)
    except Exception as e:
        return jsonify({'error': f'Invalid address: {str(e)}'})

    web3 = get_web3(rpc_url)
    if not web3.is_connected():
        return jsonify({'error': 'Cannot connect to blockchain'})

    contract = web3.eth.contract(address=contract_address, abi=ABI)
    try:
        tx = contract.functions.transferOwnership(new_owner).transact({'from': from_account, 'gas': 2000000})
        receipt = web3.eth.wait_for_transaction_receipt(tx)
        return jsonify({'success': receipt['status'] == 1})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/mint_tokens', methods=['POST'])
def mint_tokens():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')
    contract_address = data.get('contract_address', '').strip()
    to = data.get('to', '').strip()
    amount_str = data.get('amount', '').strip()
    from_account = data.get('from_account', '')

    if not contract_address:
        return jsonify({'error': 'Contract address is required'})
    if not to:
        return jsonify({'error': 'Recipient address is required'})
    if not amount_str:
        return jsonify({'error': 'Amount is required'})
    if not from_account:
        return jsonify({'error': 'From account is required'})

    try:
        amount = int(amount_str)
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'})
    except ValueError:
        return jsonify({'error': 'Invalid amount'})

    try:
        contract_address = Web3.to_checksum_address(contract_address)
        to = Web3.to_checksum_address(to)
        from_account = Web3.to_checksum_address(from_account)
    except Exception as e:
        return jsonify({'error': f'Invalid address: {str(e)}'})

    web3 = get_web3(rpc_url)
    if not web3.is_connected():
        return jsonify({'error': 'Cannot connect to blockchain'})

    contract = web3.eth.contract(address=contract_address, abi=ABI)
    try:
        tx = contract.functions.mint(to, amount).transact({'from': from_account, 'gas': 2000000})
        receipt = web3.eth.wait_for_transaction_receipt(tx)
        return jsonify({'success': receipt['status'] == 1})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/burn_tokens', methods=['POST'])
def burn_tokens():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')
    contract_address = data.get('contract_address', '').strip()
    amount_str = data.get('amount', '').strip()
    from_account = data.get('from_account', '')

    if not contract_address:
        return jsonify({'error': 'Contract address is required'})
    if not amount_str:
        return jsonify({'error': 'Amount is required'})
    if not from_account:
        return jsonify({'error': 'From account is required'})

    try:
        amount = int(amount_str)
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'})
    except ValueError:
        return jsonify({'error': 'Invalid amount'})

    try:
        contract_address = Web3.to_checksum_address(contract_address)
        from_account = Web3.to_checksum_address(from_account)
    except Exception as e:
        return jsonify({'error': f'Invalid address: {str(e)}'})

    web3 = get_web3(rpc_url)
    if not web3.is_connected():
        return jsonify({'error': 'Cannot connect to blockchain'})

    contract = web3.eth.contract(address=contract_address, abi=ABI)
    try:
        tx = contract.functions.burn(amount).transact({'from': from_account, 'gas': 2000000})
        receipt = web3.eth.wait_for_transaction_receipt(tx)
        return jsonify({'success': receipt['status'] == 1})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/transfer_tokens', methods=['POST'])
def transfer_tokens():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')
    contract_address = data.get('contract_address', '').strip()
    to = data.get('to', '').strip()
    amount_str = data.get('amount', '').strip()
    from_account = data.get('from_account', '')

    if not contract_address:
        return jsonify({'error': 'Contract address is required'})
    if not to:
        return jsonify({'error': 'Recipient address is required'})
    if not amount_str:
        return jsonify({'error': 'Amount is required'})
    if not from_account:
        return jsonify({'error': 'From account is required'})

    try:
        amount = int(amount_str)
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'})
    except ValueError:
        return jsonify({'error': 'Invalid amount'})

    try:
        contract_address = Web3.to_checksum_address(contract_address)
        to = Web3.to_checksum_address(to)
        from_account = Web3.to_checksum_address(from_account)
    except Exception as e:
        return jsonify({'error': f'Invalid address: {str(e)}'})

    web3 = get_web3(rpc_url)
    if not web3.is_connected():
        return jsonify({'error': 'Cannot connect to blockchain'})

    contract = web3.eth.contract(address=contract_address, abi=ABI)
    try:
        tx = contract.functions.transfer(to, amount).transact({'from': from_account, 'gas': 2000000})
        receipt = web3.eth.wait_for_transaction_receipt(tx)
        return jsonify({'success': receipt['status'] == 1})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/send_eth', methods=['POST'])
def send_eth():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')
    to = data.get('to', '').strip()
    amount_str = data.get('amount', '').strip()
    from_account = data.get('from_account', '')

    if not to:
        return jsonify({'error': 'Recipient address is required'})
    if not amount_str:
        return jsonify({'error': 'Amount is required'})
    if not from_account:
        return jsonify({'error': 'From account is required'})

    try:
        amount = float(amount_str)
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'})
    except ValueError:
        return jsonify({'error': 'Invalid amount'})

    try:
        to = Web3.to_checksum_address(to)
        from_account = Web3.to_checksum_address(from_account)
    except Exception as e:
        return jsonify({'error': f'Invalid address: {str(e)}'})

    web3 = get_web3(rpc_url)
    if not web3.is_connected():
        return jsonify({'error': 'Cannot connect to blockchain'})

    amount_wei = web3.to_wei(amount, 'ether')
    try:
        tx = web3.eth.send_transaction({'from': from_account, 'to': to, 'value': amount_wei, 'gas': 21000})
        receipt = web3.eth.wait_for_transaction_receipt(tx)
        return jsonify({'success': receipt['status'] == 1})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_token_balance', methods=['POST'])
def get_token_balance():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')
    contract_address = data.get('contract_address', '').strip()
    address = data.get('address', '').strip()

    if not contract_address:
        return jsonify({'error': 'Contract address is required'})
    if not address:
        return jsonify({'error': 'Address is required'})

    try:
        contract_address = Web3.to_checksum_address(contract_address)
        address = Web3.to_checksum_address(address)
    except Exception as e:
        return jsonify({'error': f'Invalid address: {str(e)}'})

    web3 = get_web3(rpc_url)
    if not web3.is_connected():
        return jsonify({'error': 'Cannot connect to blockchain'})

    contract = web3.eth.contract(address=contract_address, abi=ABI)
    try:
        balance = contract.functions.balanceOf(address).call()
        return jsonify({'balance': str(balance)})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_transfers', methods=['POST'])
def get_transfers():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')
    contract_address = data.get('contract_address', '').strip()

    if not contract_address:
        return jsonify({'error': 'Contract address is required'})

    try:
        contract_address = Web3.to_checksum_address(contract_address)
    except Exception as e:
        return jsonify({'error': f'Invalid contract address: {str(e)}'})

    web3 = get_web3(rpc_url)
    if not web3.is_connected():
        return jsonify({'error': 'Cannot connect to blockchain'})

    contract = web3.eth.contract(address=contract_address, abi=ABI)
    try:
        events = contract.events.Transfer.get_logs(fromBlock=0)
        transfers = []
        for event in events:
            transfers.append({
                'from': event.args['from'],
                'to': event.args['to'],
                'value': str(event.args['value'])
            })
        return jsonify({'transfers': transfers})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_contract_info', methods=['POST'])
def get_contract_info():
    data = request.json
    rpc_url = data.get('rpc_url', 'http://127.0.0.1:7546')
    contract_address = data.get('contract_address', '').strip()

    if not contract_address:
        return jsonify({'error': 'Contract address is required'})

    try:
        contract_address = Web3.to_checksum_address(contract_address)
    except Exception as e:
        return jsonify({'error': f'Invalid contract address: {str(e)}'})

    web3 = get_web3(rpc_url)
    if not web3.is_connected():
        return jsonify({'error': 'Cannot connect to blockchain'})

    contract = web3.eth.contract(address=contract_address, abi=ABI)
    try:
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        total_supply = contract.functions.totalSupply().call()
        owner = contract.functions.owner().call()
        return jsonify({
            'name': name,
            'symbol': symbol,
            'decimals': decimals,
            'total_supply': str(total_supply),
            'owner': owner
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)