"""Wallet management for Avalanche transactions."""

import json
import os
import secrets
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from eth_account import Account
from web3 import Web3
import base64


class WalletManager:
    """Manage Avalanche wallets with encryption support."""
    
    def __init__(self):
        """Initialize wallet manager."""
        # Enable unaudited HD wallet features for account generation
        Account.enable_unaudited_hdwallet_features()
    
    def create_wallet(self, password: str, keystore_file: str = "avax_key.json") -> str:
        """
        Create a new wallet and save encrypted keystore.
        
        Args:
            password: Password to encrypt the keystore
            keystore_file: Path to save the encrypted keystore
        
        Returns:
            Wallet address
        """
        # Generate a new private key
        private_key = secrets.token_hex(32)
        account = Account.from_key(private_key)
        
        # Create encrypted keystore
        self._save_encrypted_key(private_key, password, keystore_file)
        
        return account.address
    
    def load_wallet(self, keystore_file: str, password: str) -> str:
        """
        Load wallet from encrypted keystore.
        
        Args:
            keystore_file: Path to encrypted keystore
            password: Password to decrypt the keystore
        
        Returns:
            Wallet address
        """
        private_key = self._load_encrypted_key(keystore_file, password)
        account = Account.from_key(private_key)
        return account.address
    
    def get_private_key(self, keystore_file: str = None, password: str = None) -> str:
        """
        Get private key from environment variable or keystore.
        
        Args:
            keystore_file: Path to encrypted keystore (optional)
            password: Password to decrypt keystore (optional)
        
        Returns:
            Private key as hex string
        """
        # First, try environment variable
        env_key = os.getenv("PRIVATE_KEY")
        if env_key:
            # Ensure it's properly formatted
            if env_key.startswith("0x"):
                return env_key
            else:
                return f"0x{env_key}"
        
        # Fall back to keystore file
        if keystore_file and password:
            return self._load_encrypted_key(keystore_file, password)
        
        # Try default keystore
        default_keystore = "avax_key.json"
        if Path(default_keystore).exists() and password:
            return self._load_encrypted_key(default_keystore, password)
        
        raise ValueError(
            "No private key found. Set PRIVATE_KEY environment variable or "
            "provide keystore file with password."
        )
    
    def get_address_from_env(self) -> str:
        """Get wallet address from PRIVATE_KEY environment variable."""
        private_key = os.getenv("PRIVATE_KEY")
        if not private_key:
            raise ValueError("PRIVATE_KEY environment variable not set")
        
        if not private_key.startswith("0x"):
            private_key = f"0x{private_key}"
        
        account = Account.from_key(private_key)
        return account.address
    
    def get_account(self, keystore_file: str = None, password: str = None) -> Account:
        """
        Get Web3 account object for signing transactions.
        
        Args:
            keystore_file: Path to encrypted keystore (optional)
            password: Password to decrypt keystore (optional)
        
        Returns:
            Web3 Account object
        """
        private_key = self.get_private_key(keystore_file, password)
        return Account.from_key(private_key)
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def _save_encrypted_key(self, private_key: str, password: str, keystore_file: str) -> None:
        """Save private key to encrypted keystore file."""
        # Generate salt for key derivation
        salt = os.urandom(16)
        
        # Derive encryption key from password
        key = self._derive_key(password, salt)
        
        # Encrypt private key
        f = Fernet(key)
        encrypted_key = f.encrypt(private_key.encode())
        
        # Save to file
        keystore_data = {
            "encrypted_key": base64.b64encode(encrypted_key).decode(),
            "salt": base64.b64encode(salt).decode(),
            "version": 1
        }
        
        with open(keystore_file, 'w') as f:
            json.dump(keystore_data, f, indent=2)
        
        # Set secure file permissions (owner read/write only)
        os.chmod(keystore_file, 0o600)
    
    def _load_encrypted_key(self, keystore_file: str, password: str) -> str:
        """Load private key from encrypted keystore file."""
        if not Path(keystore_file).exists():
            raise FileNotFoundError(f"Keystore file '{keystore_file}' not found")
        
        try:
            with open(keystore_file) as f:
                keystore_data = json.load(f)
            
            # Extract data
            encrypted_key = base64.b64decode(keystore_data["encrypted_key"])
            salt = base64.b64decode(keystore_data["salt"])
            
            # Derive decryption key
            key = self._derive_key(password, salt)
            
            # Decrypt private key
            f = Fernet(key)
            private_key = f.decrypt(encrypted_key).decode()
            
            # Ensure proper formatting
            if not private_key.startswith("0x"):
                private_key = f"0x{private_key}"
            
            return private_key
        
        except Exception as e:
            raise ValueError(f"Failed to decrypt keystore: {e}")
    
    def validate_private_key(self, private_key: str) -> bool:
        """Validate that a private key is properly formatted."""
        try:
            if not private_key.startswith("0x"):
                private_key = f"0x{private_key}"
            
            # Try to create account to validate
            Account.from_key(private_key)
            return True
        except Exception:
            return False