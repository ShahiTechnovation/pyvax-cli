"""
Python Stakeable Token Contract
===============================

ERC-20 style token in Python with:
- Minting
- Staking system
- Transfer functionality
- Dynamic reward rate adjustment
"""

from avax_cli.py_contracts import PySmartContract

class StakeToken(PySmartContract):
    def __init__(self):
        super().__init__()
        
        # Token metadata
        self.name = self.state_var("name", "StakeableToken")
        self.symbol = self.state_var("symbol", "STK")
        self.decimals = self.state_var("decimals", 18)
        self.total_supply = self.state_var("total_supply", 1000000)

        # Owner and contract state
        self.owner = self.state_var("owner", 1)
        self.is_paused = self.state_var("is_paused", 0)
        
        # Balances (simplified - in real implementation would use mappings)
        self.owner_balance = self.state_var("owner_balance", 1000000)
        self.user_balance = self.state_var("user_balance", 0)
        
        # Staking system
        self.user_stake = self.state_var("user_stake", 0)
        self.user_reward = self.state_var("user_reward", 0)
        self.reward_rate = self.state_var("reward_rate", 10)

    # -------------------
    # View functions
    # -------------------
    @view_function
    def get_name(self) -> str:
        return self.name

    @view_function
    def get_symbol(self) -> str:
        return self.symbol

    @view_function
    def get_decimals(self) -> int:
        return self.decimals

    @view_function
    def get_total_supply(self) -> int:
        return self.total_supply

    @view_function
    def balance_of(self, account: int) -> int:
        if account == 1:  # Owner
            return self.owner_balance
        else:  # User
            return self.user_balance

    @view_function
    def stake_of(self, account: int) -> int:
        if account == 1:
            return 0  # Owner doesn't stake
        return self.user_stake

    @view_function
    def reward_of(self, account: int) -> int:
        if account == 1:
            return 0  # Owner doesn't get rewards
        return self.user_reward

    @view_function
    def get_reward_rate(self) -> int:
        return self.reward_rate

    # -------------------
    # Core token functions
    # -------------------
    @public_function
    def transfer(self, to: int, amount: int):
        """Transfer tokens from owner to user (simplified)"""
        if self.is_paused == 1:
            self.event("TransferFailed", "Contract is paused")
            return
        
        if self.owner_balance >= amount:
            self.owner_balance = self.owner_balance - amount
            self.user_balance = self.user_balance + amount
            self.event("Transfer", amount, to)

    @public_function
    def mint(self, amount: int):
        """Mint new tokens (owner only)"""
        self.total_supply = self.total_supply + amount
        self.owner_balance = self.owner_balance + amount
        self.event("Mint", amount, self.total_supply)

    # -------------------
    # Staking functions
    # -------------------
    @public_function
    def stake(self, amount: int):
        """Stake tokens to earn rewards"""
        if self.is_paused == 1:
            self.event("StakeFailed", "Contract is paused")
            return
            
        if self.user_balance >= amount:
            self.user_balance = self.user_balance - amount
            self.user_stake = self.user_stake + amount

            # Calculate reward instantly (simple model)
            reward = (amount * self.reward_rate) // 100
            self.user_reward = self.user_reward + reward
            self.event("Staked", amount, reward)

    @public_function
    def unstake(self, amount: int):
        """Unstake tokens and claim rewards"""
        if self.user_stake >= amount:
            self.user_stake = self.user_stake - amount
            self.user_balance = self.user_balance + amount

            # Add rewards to balance
            reward = self.user_reward
            self.user_balance = self.user_balance + reward
            self.user_reward = 0
            self.event("Unstaked", amount, reward)

    # -------------------
    # Dynamic functions (Owner only)
    # -------------------
    @public_function
    def set_reward_rate(self, new_rate: int):
        """Dynamically update staking reward rate (only owner)"""
        self.reward_rate = new_rate
        self.event("RewardRateUpdated", new_rate)

    @public_function
    def pause(self):
        """Pause contract operations (owner only)"""
        self.is_paused = 1
        self.event("ContractPaused")

    @public_function
    def unpause(self):
        """Unpause contract operations (owner only)"""
        self.is_paused = 0
        self.event("ContractUnpaused")
