"""
DeFiContract - Enhanced DeFi savings pool in Python
Compatible with complex DeFi applications!
"""

from avax_cli.py_contracts import PySmartContract

class Defi(PySmartContract):
    """Enhanced DeFi savings pool with proper address handling and mapping support."""

    def __init__(self):
        """Set up the DeFi system."""
        super().__init__()
        
        # Admin of the contract (address type)
        self.admin = self.state_var("admin", self.msg_sender())
        
        # User balances mapping (address -> uint256)
        self.balances = self.state_var("balances", {})
        
        # Total deposits in the pool
        self.total_deposits = self.state_var("total_deposits", 0)
        
        # Interest rate (basis points: 500 = 5%)
        self.interest_rate = self.state_var("interest_rate", 500)
        
        # Record the last time someone deposited (for interest calculation)
        self.last_update = self.state_var("last_update", {})
    
    @public_function
    def deposit(self, amount: int):
        """Deposit tokens into the DeFi pool."""
        sender = self.msg_sender()
        
        self.require(amount > 0, "Deposit amount must be greater than 0")
        
        # Update interest before changing balance
        self._apply_interest(sender)
        
        # Increase sender balance using mapping access
        current_balance = self.balances.get(sender, 0)
        self.balances[sender] = current_balance + amount
        self.total_deposits = self.total_deposits + amount
        self.last_update[sender] = self.block_number()
        
        self.event("Deposit", sender, amount)
    
    @public_function
    def withdraw(self, amount: int):
        """Withdraw tokens from the DeFi pool."""
        sender = self.msg_sender()
        
        # Apply interest before withdrawal
        self._apply_interest(sender)
        
        current_balance = self.balances.get(sender, 0)
        self.require(current_balance >= amount, "Insufficient balance")
        
        self.balances[sender] = current_balance - amount
        self.total_deposits = self.total_deposits - amount
        self.last_update[sender] = self.block_number()
        
        self.event("Withdraw", sender, amount)
    
    @view_function
    def balance_of(self, user: str) -> int:
        """Check the balance of a user (including interest)."""
        # Apply pending interest in a read-only way
        stored = self.balances.get(user, 0)
        if stored == 0:
            return 0
            
        last = self.last_update.get(user, self.block_number())
        
        # Calculate interest using basis points: rate/10000 * principal * time
        blocks_passed = self.block_number() - last
        if blocks_passed > 0:
            interest = stored * self.interest_rate * blocks_passed // 100000  # basis points calculation
            return stored + interest
        return stored
    
    @view_function
    def get_total_deposits(self) -> int:
        """Check total tokens in the pool."""
        return self.total_deposits
    
    @public_function
    def set_interest_rate(self, new_rate: int):
        """Change interest rate (only admin)."""
        sender = self.msg_sender()
        self.require(sender == self.admin, "Only admin can change rate")
        self.require(new_rate <= 10000, "Rate cannot exceed 100%")
        
        self.interest_rate = new_rate
        self.event("RateChanged", new_rate)
    
    def _apply_interest(self, user: str):
        """Internal: apply interest for a user before updating balances."""
        stored = self.balances.get(user, 0)
        if stored == 0:
            self.last_update[user] = self.block_number()
            return
        
        last = self.last_update.get(user, self.block_number())
        blocks_passed = self.block_number() - last
        if blocks_passed > 0:
            # Interest accumulation using basis points
            interest = stored * self.interest_rate * blocks_passed // 100000
            if interest > 0:
                self.balances[user] = stored + interest
                self.total_deposits = self.total_deposits + interest
                self.event("InterestApplied", user, interest)
            self.last_update[user] = self.block_number()
