# PyVax - Avalanche Smart Contract CLI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**PyVax** is a production-ready CLI tool for deploying Solidity and Python smart contracts to Avalanche C-Chain. It features a unique **Python-to-EVM transpiler** that allows you to write smart contracts in Python and deploy them directly to the blockchain.

## 🚀 Features

- **Python Smart Contracts**: Write smart contracts in Python and transpile them to EVM bytecode
- **Solidity Support**: Full support for Solidity contract compilation and deployment
- **Multi-Network**: Deploy to Avalanche Fuji testnet or mainnet
- **Secure Wallet Management**: Encrypted keystore with PBKDF2 encryption
- **Gas Estimation**: Accurate gas estimation before deployment
- **Rich CLI Interface**: Beautiful command-line interface with progress indicators
- **Deployment Tracking**: Automatic tracking of deployed contracts

## 📦 Installation

### Using pip

```bash
pip install -e .
```

### Using pip with requirements.txt

```bash
pip install -r requirements.txt
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## 🔧 Quick Start

### 1. Initialize a New Project

```bash
python -m avax_cli.cli init my_project
cd my_project
```

This creates a new project with:
- Sample Python and Solidity contracts
- Default configuration file
- Deployment scripts

### 2. Create a Wallet

```bash
python -m avax_cli.cli wallet new
```

This will:
- Generate a new encrypted wallet
- Save it as `avax_key.json`
- Display your wallet address

**⚠️ Important**: Fund your wallet with AVAX before deploying contracts!

### 3. Compile Contracts

```bash
python -m avax_cli.cli compile
```

This compiles both Python and Solidity contracts in the `contracts/` directory.

### 4. Deploy Contracts

```bash
# Deploy to Fuji testnet (default)
python -m avax_cli.cli deploy SimpleStorage

# Deploy to mainnet
python -m avax_cli.cli deploy SimpleStorage --network mainnet

# Deploy with constructor arguments
python -m avax_cli.cli deploy SimpleStorage --args '[42]'

# Dry run (estimate gas only)
python -m avax_cli.cli deploy SimpleStorage --dry-run
```

## 🐍 Python Smart Contracts

PyVax allows you to write smart contracts in Python using a special syntax:

```python
from avax_cli.py_contracts import PySmartContract

class SimpleStorage(PySmartContract):
    """Simple storage contract in Python."""
    
    def __init__(self):
        super().__init__()
        self.stored_data = self.state_var("stored_data", 0)
    
    @public_function
    def set(self, value: int):
        """Set stored data."""
        self.stored_data = value
        self.event("DataStored", value)
    
    @view_function
    def get(self) -> int:
        """Get stored data."""
        return self.stored_data
```

### Python Contract Features

- **State Variables**: Use `self.state_var(name, initial_value)`
- **Public Functions**: Use `@public_function` decorator
- **View Functions**: Use `@view_function` decorator
- **Events**: Use `self.event(name, *params)`
- **Basic Types**: Support for `int`, `str`, and basic operations

## 📋 CLI Commands

### Project Management

```bash
# Initialize new project
avax-cli init <project_name> [--force]

# Compile contracts
avax-cli compile [--contracts contracts/] [--output build/]
```

### Wallet Management

```bash
# Create new wallet
avax-cli wallet new [--password PASSWORD] [--keystore avax_key.json]

# Show wallet info
avax-cli wallet show [--keystore avax_key.json]
```

### Contract Deployment

```bash
# Deploy contract
avax-cli deploy <contract_name> [OPTIONS]

# Options:
#   --args TEXT          Constructor arguments as JSON array
#   --config TEXT        Configuration file path
#   --dry-run           Estimate gas without deploying
#   --network TEXT      Override network (fuji/mainnet)
```

## ⚙️ Configuration

### Network Configuration (`avax_config.json`)

```json
{
  "network": "fuji",
  "rpc_url": "https://api.avax-test.network/ext/bc/C/rpc",
  "chain_id": 43113,
  "explorer_api_key": ""
}
```

### Supported Networks

| Network | Chain ID | RPC URL |
|---------|----------|---------|
| Fuji (Testnet) | 43113 | https://api.avax-test.network/ext/bc/C/rpc |
| Mainnet | 43114 | https://api.avax.network/ext/bc/C/rpc |

## 🔐 Security

### Wallet Security

- Wallets are encrypted using PBKDF2 with SHA-256
- Private keys are never stored in plain text
- Support for environment variable (`PRIVATE_KEY`) for CI/CD

### Best Practices

1. **Never commit private keys** to version control
2. **Use strong passwords** for wallet encryption
3. **Backup your keystore files** securely
4. **Test on Fuji testnet** before mainnet deployment

## 📁 Project Structure

```
my-project/
├── contracts/           # Smart contracts (.sol and .py files)
│   ├── SimpleStorage.py
│   └── SimpleStorage.sol
├── build/              # Compiled contract artifacts
├── scripts/            # Deployment scripts
│   └── deploy.py
├── avax_config.json    # Network configuration
└── deployments.json   # Deployment history
```

## 🛠️ Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black avax_cli/
isort avax_cli/
```

### Type Checking

```bash
mypy avax_cli/
```

## 📖 Examples

### Example 1: Counter Contract

```python
class Counter(PySmartContract):
    def __init__(self):
        super().__init__()
        self.count = self.state_var("count", 0)
    
    @public_function
    def increment(self):
        self.count = self.count + 1
        self.event("Incremented", self.count)
    
    @view_function
    def get_count(self) -> int:
        return self.count
```

### Example 2: Deployment Script

```python
#!/usr/bin/env python3
from avax_cli.deployer import deploy_contract
from avax_cli.wallet import WalletManager
import json

# Load configuration
with open("avax_config.json") as f:
    config = json.load(f)

# Deploy contract
wallet = WalletManager()
result = deploy_contract(
    contract_name="Counter",
    constructor_args=[],
    config=config,
    wallet=wallet
)

print(f"Contract deployed at: {result['address']}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/pyvax/avax-cli/issues)
- **Documentation**: [GitHub README](https://github.com/pyvax/avax-cli#readme)
- **Avalanche Docs**: [Official Documentation](https://docs.avax.network/)

## 🔗 Links

- [Avalanche Network](https://www.avax.network/)
- [Avalanche C-Chain Explorer](https://snowtrace.io/)
- [Fuji Testnet Faucet](https://faucet.avax.network/)

---

**⚡ Happy Building on Avalanche! ⚡**