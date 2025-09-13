"""
MintableToken - ERC-20 style token with admin-controlled minting
Written in Python for AVAX CLI
"""

from avax_cli.py_contracts import PySmartContract

class MintableToken(PySmartContract):
    """ERC-20 style mintable token contract."""

    def __init__(self):
        super().__init__()
        
        # Token metadata
        self.name = self.state_var("name", "MintableToken")
        self.symbol = self.state_var("symbol", "MINT")
        self.decimals = self.state_var("decimals", 18)
        
        # Admin address
        self.admin = self.state_var("admin", self.msg_sender())
        
        # Total supply of tokens
        self.total_supply = self.state_var("total_supply", 0)
        
        # Balances mapping (address -> uint256)
        self.balances = self.state_var("balances", {})

    @public_function
    def transfer(self, to: str, amount: int):
        """Transfer tokens to another address."""
        sender = self.msg_sender()
        self.require(amount > 0, "Amount must be positive")
        
        sender_balance = self.balances.get(sender, 0)
        self.require(sender_balance >= amount, "Insufficient balance")
        
        # Adjust balances
        self.balances[sender] = sender_balance - amount
        self.balances[to] = self.balances.get(to, 0) + amount
        
        self.event("Transfer", sender, to, amount)

    @public_function
    def mint(self, to: str, amount: int):
        """Mint new tokens (only admin)."""
        sender = self.msg_sender()
        self.require(sender == self.admin, "Only admin can mint")
        self.require(amount > 0, "Mint amount must be positive")
        
        # Increase supply and receiver balance
        self.total_supply = self.total_supply + amount
        self.balances[to] = self.balances.get(to, 0) + amount
        
        self.event("Mint", to, amount)

    @view_function
    def balance_of(self, user: str) -> int:
        """Check the balance of a user."""
        return self.balances.get(user, 0)

    @view_function
    def get_total_supply(self) -> int:
        """Get the total token supply."""
        return self.total_supply

    @view_function
    def get_name(self) -> str:
        """Get token name."""
        return self.name

    @view_function
    def get_symbol(self) -> str:
        """Get token symbol."""
        return self.symbol

    @view_function
    def get_decimals(self) -> int:
        """Get token decimals."""
        return self.decimals
