# 🐍 PyVax - Python Smart Contracts for Avalanche

**Write smart contracts in Python. Deploy to Avalanche. No Solidity required.**

PyVax is a revolutionary CLI tool that enables Python developers to create blockchain applications using familiar Python syntax. Deploy ERC-20 tokens, voting systems, and complex DeFi protocols directly to Avalanche C-Chain.

## 🌟 **Key Features**

- 🐍 **Pure Python Contracts**: Write smart contracts in Python syntax
- ⚡ **One-Command Deployment**: Deploy to Avalanche with single command
- 🔧 **Python-to-EVM Transpiler**: Converts Python code to EVM bytecode
- 🌐 **Multi-Network Support**: Fuji testnet and Avalanche mainnet
- 💰 **Built-in Wallet Management**: Secure wallet creation and management
- 🔍 **Contract Interaction**: Call functions, send transactions, check balances
- 📊 **Rich CLI Interface**: Beautiful terminal output with progress indicators

## 🚀 **Quick Start**

### 1. Initialize Project
```bash
python -m avax_cli.cli init my_project
cd my_project
```

### 2. Set Private Key
```bash
# PowerShell
$env:PRIVATE_KEY="your_private_key_here"
```

### 3. Write Python Contract
```python
# contracts/MyToken.py
from avax_cli.py_contracts import PySmartContract

class MyToken(PySmartContract):
    def __init__(self):
        super().__init__()
        self.name = self.state_var("name", "MyToken")
        self.total_supply = self.state_var("total_supply", 1000000)
        self.balances = self.state_var("balances", {})
        
        owner = self.msg_sender()
        self.balances[owner] = self.total_supply
    
    @view_function
    def get_name(self) -> str:
        return self.name
    
    @public_function
    def transfer(self, to: str, amount: int):
        sender = self.msg_sender()
        if self.balances.get(sender, 0) < amount:
            raise Exception("Insufficient balance")
        
        self.balances[sender] -= amount
        self.balances[to] = self.balances.get(to, 0) + amount
        self.event("Transfer", sender, to, amount)
```

### 4. Deploy to Avalanche
```bash
python -m avax_cli.cli compile
python -m avax_cli.cli deploy MyToken
```

**🎉 Your Python smart contract is now live on Avalanche!**

## 📋 **Complete Command Reference**

### **Project Management**
```bash
# Initialize new project
python -m avax_cli.cli init <project_name>

# Compile all contracts
python -m avax_cli.cli compile

# Deploy contract
python -m avax_cli.cli deploy <ContractName>

# Deploy with dry run (gas estimation)
python -m avax_cli.cli deploy <ContractName> --dry-run
```

### **Wallet Management**
```bash
# Create new wallet
python -m avax_cli.cli wallet new

# Show wallet info
python -m avax_cli.cli wallet info
```

### **Contract Interaction**
```bash
# View contract information
python -m avax_cli.cli info <ContractName>

# Call view function (free)
python -m avax_cli.cli interact <ContractName> <function_name> --view

# Call view function with arguments
python -m avax_cli.cli interact <ContractName> balance_of --args "0x123..." --view

# Send transaction (costs gas)
python -m avax_cli.cli interact <ContractName> transfer --args "0x456...,1000"

# Mint tokens (if you're the owner)
python -m avax_cli.cli interact <ContractName> mint --args "1000"
```

### **Staking Operations** (for StakeToken contracts)
```bash
# Stake tokens
python -m avax_cli.cli interact StakeToken stake --args "100"

# Check staked balance
python -m avax_cli.cli interact StakeToken stakeOf --args "0x123..." --view

# Check rewards
python -m avax_cli.cli interact StakeToken rewardOf --args "0x123..." --view

# Unstake tokens (includes rewards)
python -m avax_cli.cli interact StakeToken unstake --args "50"

# Set reward rate (owner only)
python -m avax_cli.cli interact StakeToken setRewardRate --args "15"
```

### **Admin Functions** (owner-only)
```bash
# Pause contract
python -m avax_cli.cli interact <ContractName> pause

# Unpause contract
python -m avax_cli.cli interact <ContractName> unpause

# Mint new tokens
python -m avax_cli.cli interact <ContractName> mint --args "1000"
```

## 🔧 **Shortcut Commands**

Create shortcuts for easier usage:
```bash
# Create shortcut files
.\avax.bat compile
.\avax.bat deploy MyToken
.\avax.bat info StakeToken
.\avax.bat interact StakeToken name --view
```

## 📚 **Example Contracts**

### **Simple Token**
```python
class SimpleToken(PySmartContract):
    def __init__(self):
        super().__init__()
        self.name = self.state_var("name", "SimpleToken")
        self.symbol = self.state_var("symbol", "SIM")
        self.total_supply = self.state_var("total_supply", 1000000)
        self.balances = self.state_var("balances", {})
        
        owner = self.msg_sender()
        self.balances[owner] = self.total_supply
    
    @view_function
    def balance_of(self, account: str) -> int:
        return self.balances.get(account, 0)
    
    @public_function
    def transfer(self, to: str, amount: int):
        sender = self.msg_sender()
        if self.balances.get(sender, 0) < amount:
            raise Exception("Insufficient balance")
        
        self.balances[sender] -= amount
        self.balances[to] = self.balances.get(to, 0) + amount
        self.event("Transfer", sender, to, amount)
```

### **Voting System**
```python
class VotingContract(PySmartContract):
    def __init__(self):
        super().__init__()
        self.admin = self.state_var("admin", self.msg_sender())
        self.voting_open = self.state_var("voting_open", True)
        self.candidates = self.state_var("candidates", [])
        self.vote_counts = self.state_var("vote_counts", {})
        self.has_voted = self.state_var("has_voted", {})
    
    @public_function
    def add_candidate(self, name: str):
        if self.msg_sender() != self.admin:
            raise Exception("Only admin can add candidates")
        
        self.candidates.append(name)
        self.vote_counts[name] = 0
        self.event("CandidateAdded", name)
    
    @public_function
    def vote(self, candidate_name: str):
        sender = self.msg_sender()
        
        if not self.voting_open:
            raise Exception("Voting is closed")
        if self.has_voted.get(sender, False):
            raise Exception("Already voted")
        if candidate_name not in self.candidates:
            raise Exception("Invalid candidate")
        
        self.vote_counts[candidate_name] += 1
        self.has_voted[sender] = True
        self.event("VoteCast", sender, candidate_name)
    
    @view_function
    def get_winner(self) -> str:
        winner = ""
        max_votes = -1
        for candidate in self.candidates:
            votes = self.vote_counts.get(candidate, 0)
            if votes > max_votes:
                max_votes = votes
                winner = candidate
        return winner
```

## 🎯 **Real-World Examples**

### **Deploy and Interact with Token**
```bash
# 1. Create and deploy token
python -m avax_cli.cli init TokenProject
cd TokenProject
# (Write your token contract)
python -m avax_cli.cli compile
python -m avax_cli.cli deploy MyToken

# 2. Check token details
python -m avax_cli.cli interact MyToken name --view
python -m avax_cli.cli interact MyToken totalSupply --view
python -m avax_cli.cli interact MyToken balanceOf --args "0x7F79991446a8Bf4e77bD96Afad009171C68Ad34a" --view

# 3. Transfer tokens
python -m avax_cli.cli interact MyToken transfer --args "0x456...,1000"

# 4. Check new balance
python -m avax_cli.cli interact MyToken balanceOf --args "0x456..." --view
```

### **Staking Workflow**
```bash
# 1. Deploy staking contract
python -m avax_cli.cli deploy StakeToken

# 2. Check initial state
python -m avax_cli.cli interact StakeToken totalSupply --view
python -m avax_cli.cli interact StakeToken rewardRate --view

# 3. Stake tokens
python -m avax_cli.cli interact StakeToken stake --args "1000"

# 4. Check staked amount
python -m avax_cli.cli interact StakeToken stakedBalance --args "YOUR_ADDRESS" --view

# 5. Wait some time, then check rewards
python -m avax_cli.cli interact StakeToken getReward --args "YOUR_ADDRESS" --view

# 6. Unstake and claim rewards
python -m avax_cli.cli interact StakeToken unstake --args "500"
```

## 🌐 **Network Information**

### **Avalanche Fuji Testnet** (Default)
- **RPC URL**: `https://api.avax-test.network/ext/bc/C/rpc`
- **Chain ID**: `43113`
- **Explorer**: [testnet.snowtrace.io](https://testnet.snowtrace.io)
- **Faucet**: [faucet.avax.network](https://faucet.avax.network)

### **Avalanche Mainnet**
- **RPC URL**: `https://api.avax.network/ext/bc/C/rpc`
- **Chain ID**: `43114`
- **Explorer**: [snowtrace.io](https://snowtrace.io)

## 🔍 **Deployed Contract Examples**

### **Live StakeToken Contract**
- **Address**: `0x0C1E83383998caf4A32451764f3A7Fd6eaB358Dc`
- **Network**: Avalanche Fuji Testnet
- **Features**: ERC-20 + Staking with 10% rewards
- **View on Explorer**: [testnet.snowtrace.io](https://testnet.snowtrace.io/address/0x0C1E83383998caf4A32451764f3A7Fd6eaB358Dc)

```bash
# Interact with live contract
python -m avax_cli.cli interact StakeToken name --view
python -m avax_cli.cli interact StakeToken totalSupply --view
python -m avax_cli.cli interact StakeToken balanceOf --args "0x7F79991446a8Bf4e77bD96Afad009171C68Ad34a" --view
```

## 🛠️ **Development Tips**

### **Python Contract Best Practices**
1. **Always call `super().__init__()`** in constructor
2. **Use `@view_function`** for read-only operations (free)
3. **Use `@public_function`** for state changes (costs gas)
4. **Initialize state variables** with `self.state_var()`
5. **Emit events** for important actions with `self.event()`
6. **Add input validation** to prevent errors

### **Common Patterns**
```python
# State variable
self.balance = self.state_var("balance", 0)

# Access control
if self.msg_sender() != self.owner:
    raise Exception("Access denied")

# Event logging
self.event("Transfer", sender, recipient, amount)

# Safe math
if balance < amount:
    raise Exception("Insufficient funds")
```

### **Debugging Tips**
- Use `--dry-run` flag to test deployments without spending gas
- Check contract info with `info` command before interacting
- Use `--view` flag for read-only function calls
- Verify bytecode on explorer matches expected functionality

## 📦 **Installation & Setup**

### **Requirements**
- Python 3.8+
- Windows (PowerShell support)
- AVAX for gas fees

### **Environment Setup**
```bash
# Clone or download PyVax
cd pyvax

# Install dependencies (if needed)
pip install -r requirements.txt

# Set private key
$env:PRIVATE_KEY="your_private_key_here"

# Initialize project
python -m avax_cli.cli init my_project
```

## 🚨 **Important Notes**

### **Security**
- ⚠️ **Never commit private keys** to version control
- ⚠️ **Use testnet first** before deploying to mainnet
- ⚠️ **Test thoroughly** before handling real funds
- ⚠️ **Audit contracts** before production use

### **Gas Costs**
- **Deployment**: ~0.001-0.01 AVAX depending on contract size
- **Function calls**: ~0.0001-0.001 AVAX per transaction
- **View functions**: Free (no gas cost)

### **Limitations**
- Python transpiler has some limitations with complex data types
- For production use, consider Solidity for gas optimization
- String handling in Python contracts needs improvement

## 🎉 **Success Stories**

✅ **BeginnerToken**: Simple ERC-20 token deployed successfully  
✅ **StakeToken**: Advanced staking system with rewards  
✅ **VotingContract**: Democratic voting system  
✅ **SimpleStorage**: Basic data storage contract  

## 🔗 **Resources**

- **PyVax Documentation**: This README
- **Avalanche Docs**: [docs.avax.network](https://docs.avax.network)
- **Snowtrace Explorer**: [snowtrace.io](https://snowtrace.io)
- **AVAX Faucet**: [faucet.avax.network](https://faucet.avax.network)

---

**🐍 PyVax makes blockchain development accessible to every Python developer!**

*Write Python. Deploy to Avalanche. Build the future.* ⛓️
