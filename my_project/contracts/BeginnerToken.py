"""
BeginnerToken - A simple Python smart contract for beginners
No Solidity knowledge required! Just Python.
"""

from avax_cli.py_contracts import PySmartContract

class BeginnerToken(PySmartContract):
    """A simple token contract written in pure Python."""
    
    def __init__(self):
        """Initialize the token with basic settings."""
        super().__init__()
        
        # Token information (like variables in Python)
        self.name = self.state_var("name", "BeginnerCoin")
        self.symbol = self.state_var("symbol", "BGN") 
        self.total_supply = self.state_var("total_supply", 1000000)
        
        # Track who owns how many tokens
        self.balances = self.state_var("balances", {})
        
        # The person who creates the contract gets all tokens
        self.owner = self.state_var("owner", self.msg_sender())
        self.balances[self.owner] = self.total_supply
    
    @view_function
    def get_name(self) -> str:
        """Get the token name - anyone can call this."""
        return self.name
    
    @view_function  
    def get_symbol(self) -> str:
        """Get the token symbol - anyone can call this."""
        return self.symbol
    
    @view_function
    def get_total_supply(self) -> int:
        """Get total number of tokens - anyone can call this."""
        return self.total_supply
    
    @view_function
    def balance_of(self, account: str) -> int:
        """Check how many tokens someone has - anyone can call this."""
        return self.balances.get(account, 0)
    
    @public_function
    def transfer(self, to: str, amount: int):
        """Send tokens to someone else."""
        sender = self.msg_sender()
        
        # Make sure sender has enough tokens
        if self.balances.get(sender, 0) < amount:
            raise Exception("Not enough tokens!")
        
        # Make sure amount is positive
        if amount <= 0:
            raise Exception("Amount must be positive!")
        
        # Do the transfer
        self.balances[sender] = self.balances.get(sender, 0) - amount
        self.balances[to] = self.balances.get(to, 0) + amount
        
        # Log what happened
        self.event("Transfer", sender, to, amount)
    
    @public_function
    def mint(self, amount: int):
        """Create new tokens (only owner can do this)."""
        sender = self.msg_sender()
        
        # Only the owner can create new tokens
        if sender != self.owner:
            raise Exception("Only owner can mint tokens!")
        
        if amount <= 0:
            raise Exception("Amount must be positive!")
        
        # Add new tokens to total supply and owner's balance
        self.total_supply += amount
        self.balances[self.owner] = self.balances.get(self.owner, 0) + amount
        
        # Log what happened
        self.event("Mint", self.owner, amount)
    
    @public_function
    def burn(self, amount: int):
        """Destroy some of your tokens."""
        sender = self.msg_sender()
        
        if self.balances.get(sender, 0) < amount:
            raise Exception("Not enough tokens to burn!")
        
        if amount <= 0:
            raise Exception("Amount must be positive!")
        
        # Remove tokens from circulation
        self.balances[sender] -= amount
        self.total_supply -= amount
        
        # Log what happened
        self.event("Burn", sender, amount)
