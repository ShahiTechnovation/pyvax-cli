#!/usr/bin/env python3
"""Test script for contract interaction functionality."""

import json
import os
from pathlib import Path
from web3 import Web3

def test_contract_interaction():
    """Test direct Web3 interaction with deployed StakeToken contract."""
    
    # Load deployment info
    with open("my_project/deployments.json") as f:
        deployments = json.load(f)
    
    contract_info = deployments["fuji"]["StakeToken"]
    contract_address = contract_info["address"]
    
    print(f"Testing contract at: {contract_address}")
    
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
    
    # Create contract instance
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    print(f"📋 Contract instance created")
    print(f"📋 Available functions: {[f['name'] for f in abi if f['type'] == 'function']}")
    
    # Test view functions
    try:
        # Test basic view functions
        print("\n🔍 Testing view functions:")
        
        # Test get_total_supply
        try:
            total_supply = contract.functions.get_total_supply().call()
            print(f"✅ Total Supply: {total_supply}")
        except Exception as e:
            print(f"❌ get_total_supply failed: {e}")
        
        # Test get_name
        try:
            name = contract.functions.get_name().call()
            print(f"✅ Token Name: {name}")
        except Exception as e:
            print(f"❌ get_name failed: {e}")
        
        # Test get_symbol
        try:
            symbol = contract.functions.get_symbol().call()
            print(f"✅ Token Symbol: {symbol}")
        except Exception as e:
            print(f"❌ get_symbol failed: {e}")
        
        # Test get_decimals
        try:
            decimals = contract.functions.get_decimals().call()
            print(f"✅ Token Decimals: {decimals}")
        except Exception as e:
            print(f"❌ get_decimals failed: {e}")
        
        # Test get_reward_rate
        try:
            reward_rate = contract.functions.get_reward_rate().call()
            print(f"✅ Reward Rate: {reward_rate}")
        except Exception as e:
            print(f"❌ get_reward_rate failed: {e}")
            
    except Exception as e:
        print(f"❌ Contract interaction failed: {e}")
        return
    
    print("\n✅ Contract interaction test completed!")

if __name__ == "__main__":
    test_contract_interaction()
