#!/usr/bin/env python3
"""Test script for StakeToken transaction functions (mint, stake, transfer)."""

import json
import os
from pathlib import Path
from web3 import Web3
from eth_account import Account

def test_stake_transactions():
    """Test transaction functions with deployed Solidity StakeToken contract."""
    
    # Load deployment info
    with open("my_project/deployments.json") as f:
        deployments = json.load(f)
    
    contract_info = deployments["fuji"]["StakeToken"]
    contract_address = contract_info["address"]
    
    print(f"🔗 Testing transactions on contract: {contract_address}")
    
    # Load contract ABI
    with open("my_project/build/StakeToken/StakeToken.json") as f:
        contract_data = json.load(f)
    
    abi = contract_data["abi"]
    
    # Connect to Avalanche Fuji
    rpc_url = "https://api.avax-test.network/ext/bc/C/rpc"
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    if not w3.is_connected():
        print("❌ Failed to connect to Avalanche network")
        return
    
    print("✅ Connected to Avalanche Fuji testnet")
    
    # Get private key from environment
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY environment variable not set")
        return
    
    # Create account from private key
    account = Account.from_key(private_key)
    print(f"📋 Using account: {account.address}")
    
    # Create contract instance
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    # Check current balance
    try:
        current_balance = w3.eth.get_balance(account.address)
        print(f"💰 AVAX Balance: {w3.from_wei(current_balance, 'ether'):.4f} AVAX")
        
        token_balance = contract.functions.balanceOf(account.address).call()
        print(f"🪙 Token Balance: {token_balance / 10**18:,.2f} STK")
        
        staked_balance = contract.functions.stakedBalance(account.address).call()
        print(f"🔒 Staked Balance: {staked_balance / 10**18:,.2f} STK")
        
    except Exception as e:
        print(f"❌ Error checking balances: {e}")
        return
    
    # Test functions
    print("\n🧪 Testing Contract Functions:")
    
    # Test 1: Mint tokens (owner only)
    try:
        print("\n1️⃣ Testing mint function...")
        owner = contract.functions.owner().call()
        
        if account.address.lower() == owner.lower():
            mint_amount = 1000 * 10**18  # 1000 tokens
            
            # Build transaction
            nonce = w3.eth.get_transaction_count(account.address)
            gas_price = w3.eth.gas_price
            
            mint_tx = contract.functions.mint(mint_amount).build_transaction({
                'from': account.address,
                'gas': 200000,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': 43113
            })
            
            # Sign and send
            signed_tx = account.sign_transaction(mint_tx)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            print(f"   📤 Mint transaction sent: {tx_hash.hex()}")
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
            
            if receipt.status == 1:
                print(f"   ✅ Minted 1000 STK tokens successfully!")
            else:
                print(f"   ❌ Mint transaction failed")
        else:
            print(f"   ⚠️ Skipping mint test - not contract owner")
            print(f"   Owner: {owner}")
            print(f"   Account: {account.address}")
            
    except Exception as e:
        print(f"   ❌ Mint test failed: {e}")
    
    # Test 2: Transfer tokens
    try:
        print("\n2️⃣ Testing transfer function...")
        
        # Check if we have tokens to transfer
        token_balance = contract.functions.balanceOf(account.address).call()
        
        if token_balance > 0:
            transfer_amount = min(100 * 10**18, token_balance // 2)  # Transfer 100 tokens or half balance
            recipient = "0x0000000000000000000000000000000000000001"  # Burn address for testing
            
            nonce = w3.eth.get_transaction_count(account.address)
            gas_price = w3.eth.gas_price
            
            transfer_tx = contract.functions.transfer(recipient, transfer_amount).build_transaction({
                'from': account.address,
                'gas': 100000,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': 43113
            })
            
            signed_tx = account.sign_transaction(transfer_tx)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            print(f"   📤 Transfer transaction sent: {tx_hash.hex()}")
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
            
            if receipt.status == 1:
                print(f"   ✅ Transferred {transfer_amount / 10**18:,.2f} STK successfully!")
            else:
                print(f"   ❌ Transfer transaction failed")
        else:
            print(f"   ⚠️ Skipping transfer test - no tokens to transfer")
            
    except Exception as e:
        print(f"   ❌ Transfer test failed: {e}")
    
    # Test 3: Stake tokens
    try:
        print("\n3️⃣ Testing stake function...")
        
        token_balance = contract.functions.balanceOf(account.address).call()
        
        if token_balance > 0:
            stake_amount = min(50 * 10**18, token_balance // 4)  # Stake 50 tokens or quarter balance
            
            nonce = w3.eth.get_transaction_count(account.address)
            gas_price = w3.eth.gas_price
            
            stake_tx = contract.functions.stake(stake_amount).build_transaction({
                'from': account.address,
                'gas': 150000,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': 43113
            })
            
            signed_tx = account.sign_transaction(stake_tx)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            print(f"   📤 Stake transaction sent: {tx_hash.hex()}")
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
            
            if receipt.status == 1:
                print(f"   ✅ Staked {stake_amount / 10**18:,.2f} STK successfully!")
                
                # Check staked balance
                staked_balance = contract.functions.stakedBalance(account.address).call()
                print(f"   🔒 New staked balance: {staked_balance / 10**18:,.2f} STK")
            else:
                print(f"   ❌ Stake transaction failed")
        else:
            print(f"   ⚠️ Skipping stake test - no tokens to stake")
            
    except Exception as e:
        print(f"   ❌ Stake test failed: {e}")
    
    # Final balance check
    try:
        print("\n📊 Final Balance Summary:")
        token_balance = contract.functions.balanceOf(account.address).call()
        staked_balance = contract.functions.stakedBalance(account.address).call()
        reward_balance = contract.functions.getReward(account.address).call()
        
        print(f"   🪙 Token Balance: {token_balance / 10**18:,.2f} STK")
        print(f"   🔒 Staked Balance: {staked_balance / 10**18:,.2f} STK")
        print(f"   🎁 Pending Rewards: {reward_balance / 10**18:,.6f} STK")
        
    except Exception as e:
        print(f"❌ Error checking final balances: {e}")
    
    print("\n✅ Transaction testing completed!")

if __name__ == "__main__":
    test_stake_transactions()
