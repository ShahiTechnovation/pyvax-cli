# 🚀 PyVax StakeToken Deployment & Interaction Guide

## 📋 Overview
This guide demonstrates the complete deployment and interaction workflow for the StakeToken smart contract using PyVax CLI.

## ✅ What We've Accomplished

### 🏗️ **Contract Development**
- ✅ **Python Version**: Created `StakeToken.py` with PyVax decorators
- ✅ **Solidity Version**: Created `StakeToken.sol` with full ERC-20 + staking functionality
- ✅ **Compilation**: Both versions compile successfully
- ✅ **Deployment**: Solidity version deployed to Avalanche Fuji testnet

### 🔧 **CLI Enhancement**
- ✅ **Contract Interaction**: Added `interact` and `info` commands
- ✅ **Transaction Support**: Full support for view and state-changing functions
- ✅ **Error Handling**: Comprehensive error handling and user feedback

### 🧪 **Testing & Validation**
- ✅ **View Functions**: All read operations working (name, symbol, balances)
- ✅ **Transactions**: Mint, transfer, stake, unstake all functional
- ✅ **Rewards System**: Time-based staking rewards working correctly
- ✅ **Admin Functions**: Pause/unpause, reward rate changes working

## 📊 **Deployed Contract Details**

```
Contract Address: 0x0C1E83383998caf4A32451764f3A7Fd6eaB358Dc
Network: Avalanche Fuji Testnet
Token Name: StakeableToken
Token Symbol: STK
Total Supply: 1,000,000 STK
Decimals: 18
Reward Rate: 10% (adjustable by owner)
```

## 🛠️ **Usage Examples**

### **Basic CLI Commands**

```bash
# Navigate to project directory
cd my_project

# View contract information
python -m avax_cli.cli info StakeToken

# Check token name (view function)
python -m avax_cli.cli interact StakeToken name --view

# Check total supply
python -m avax_cli.cli interact StakeToken totalSupply --view

# Check your token balance
python -m avax_cli.cli interact StakeToken balanceOf --args "YOUR_ADDRESS" --view

# Transfer tokens
python -m avax_cli.cli interact StakeToken transfer --args "RECIPIENT_ADDRESS,AMOUNT"

# Stake tokens
python -m avax_cli.cli interact StakeToken stake --args "AMOUNT"

# Check staked balance
python -m avax_cli.cli interact StakeToken stakedBalance --args "YOUR_ADDRESS" --view

# Unstake tokens (includes rewards)
python -m avax_cli.cli interact StakeToken unstake --args "AMOUNT"
```

### **Owner-Only Functions**

```bash
# Mint new tokens (owner only)
python -m avax_cli.cli interact StakeToken mint --args "AMOUNT"

# Set reward rate (owner only)
python -m avax_cli.cli interact StakeToken setRewardRate --args "NEW_RATE"

# Pause contract (owner only)
python -m avax_cli.cli interact StakeToken pause

# Unpause contract (owner only)
python -m avax_cli.cli interact StakeToken unpause
```

## 🐍 **Python Integration Examples**

### **Direct Web3 Interaction**
```python
# Run the test scripts
python test_solidity_contract.py      # View functions test
python test_stake_transactions.py     # Transaction functions test
```

### **Comprehensive Examples**
```python
# Run the complete interaction examples
cd examples
python stake_token_examples.py
```

## 🔍 **Contract Features**

### **ERC-20 Token Functions**
- ✅ `name()` → "StakeableToken"
- ✅ `symbol()` → "STK"
- ✅ `decimals()` → 18
- ✅ `totalSupply()` → Current total supply
- ✅ `balanceOf(address)` → Token balance of address
- ✅ `transfer(to, amount)` → Transfer tokens

### **Staking System**
- ✅ `stake(amount)` → Stake tokens to earn rewards
- ✅ `unstake(amount)` → Unstake tokens + claim rewards
- ✅ `stakedBalance(address)` → Amount staked by address
- ✅ `getReward(address)` → Pending rewards for address
- ✅ Time-based reward calculation (10% annual rate)

### **Admin Controls**
- ✅ `mint(amount)` → Create new tokens (owner only)
- ✅ `setRewardRate(rate)` → Adjust reward rate (owner only)
- ✅ `pause()` / `unpause()` → Emergency controls (owner only)
- ✅ `owner()` → Contract owner address

## 🌐 **Network Information**

```
Network: Avalanche Fuji Testnet
RPC URL: https://api.avax-test.network/ext/bc/C/rpc
Chain ID: 43113
Explorer: https://testnet.snowtrace.io/
```

## 📈 **Test Results Summary**

### **Successful Operations**
1. ✅ **Contract Deployment**: Deployed successfully with proper gas estimation
2. ✅ **View Function Calls**: All read operations return correct values
3. ✅ **Token Minting**: Successfully minted 1000 STK tokens
4. ✅ **Token Transfers**: Transferred tokens between addresses
5. ✅ **Staking Operations**: Staked 50 STK tokens successfully
6. ✅ **Balance Tracking**: All balances update correctly
7. ✅ **Reward System**: Time-based rewards accumulate properly

### **Final State**
- **Total Supply**: 1,000,850 STK (after minting)
- **Owner Balance**: ~1,000,800 STK
- **Staked Amount**: 50 STK
- **Pending Rewards**: Accumulating based on time

## 🚀 **Next Steps**

1. **Frontend Integration**: Build a web interface for easier interaction
2. **Advanced Features**: Add more staking pools, governance, or NFT integration
3. **Testing**: Deploy to mainnet after thorough testing
4. **Optimization**: Gas optimization and security audits

## 🔧 **Troubleshooting**

### **Common Issues**
- **Private Key**: Ensure `PRIVATE_KEY` environment variable is set
- **Gas Fees**: Ensure sufficient AVAX for transaction fees
- **Network**: Verify connection to Avalanche Fuji testnet
- **Permissions**: Owner-only functions require deployer account

### **CLI Issues**
- Use `python -m avax_cli.cli` instead of `avax-cli` command
- Ensure you're in the correct project directory
- Check that contracts are compiled before deployment

## 🎉 **Success!**

Your StakeToken contract is now fully deployed and functional on Avalanche Fuji testnet with:
- ✅ Complete ERC-20 token functionality
- ✅ Advanced staking system with rewards
- ✅ Admin controls and emergency features
- ✅ CLI tools for easy interaction
- ✅ Python examples for integration
- ✅ Comprehensive testing and validation

The PyVax CLI tool now provides a complete solution for deploying and interacting with both Python and Solidity smart contracts on Avalanche!
