#!/usr/bin/env python3
"""Test script for Solidity StakeToken contract interaction."""

import json
import os
from pathlib import Path
from web3 import Web3

def test_solidity_contract():
    """Test direct Web3 interaction with deployed Solidity StakeToken contract."""
    
    # Load deployment info
    with open("my_project/deployments.json") as f:
        deployments = json.load(f)
    
    contract_info = deployments["fuji"]["StakeToken"]
    contract_address = contract_info["address"]
    
    print(f"🔗 Testing Solidity contract at: {contract_address}")
    
    # Load contract ABI from Solidity build
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
    
    # Create contract instance
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    print(f"📋 Contract instance created")
    
    # Test view functions
    try:
        print("\n🔍 Testing Solidity contract view functions:")
        
        # Test name
        try:
            name = contract.functions.name().call()
            print(f"✅ Token Name: {name}")
        except Exception as e:
            print(f"❌ name() failed: {e}")
        
        # Test symbol
        try:
            symbol = contract.functions.symbol().call()
            print(f"✅ Token Symbol: {symbol}")
        except Exception as e:
            print(f"❌ symbol() failed: {e}")
        
        # Test decimals
        try:
            decimals = contract.functions.decimals().call()
            print(f"✅ Token Decimals: {decimals}")
        except Exception as e:
            print(f"❌ decimals() failed: {e}")
        
        # Test totalSupply
        try:
            total_supply = contract.functions.totalSupply().call()
            print(f"✅ Total Supply: {total_supply / 10**18:,.2f} STK")
        except Exception as e:
            print(f"❌ totalSupply() failed: {e}")
        
        # Test owner
        try:
            owner = contract.functions.owner().call()
            print(f"✅ Owner: {owner}")
        except Exception as e:
            print(f"❌ owner() failed: {e}")
        
        # Test reward rate
        try:
            reward_rate = contract.functions.rewardRate().call()
            print(f"✅ Reward Rate: {reward_rate}%")
        except Exception as e:
            print(f"❌ rewardRate() failed: {e}")
        
        # Test isPaused
        try:
            is_paused = contract.functions.isPaused().call()
            print(f"✅ Is Paused: {is_paused}")
        except Exception as e:
            print(f"❌ isPaused() failed: {e}")
        
        # Test balance of owner
        try:
            owner_balance = contract.functions.balanceOf(owner).call()
            print(f"✅ Owner Balance: {owner_balance / 10**18:,.2f} STK")
        except Exception as e:
            print(f"❌ balanceOf() failed: {e}")
            
    except Exception as e:
        print(f"❌ Contract interaction failed: {e}")
        return
    
    print("\n✅ Solidity contract interaction test completed!")
    print(f"\n📊 Contract Summary:")
    print(f"   • Address: {contract_address}")
    print(f"   • Network: Avalanche Fuji Testnet")
    print(f"   • Type: Solidity Smart Contract")
    print(f"   • Features: ERC-20 Token with Staking")

if __name__ == "__main__":
    test_solidity_contract()
