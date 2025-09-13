// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SimpleStorageSol {
    uint256 private storedData;
    
    event DataStored(uint256 indexed value, address indexed sender);
    
    constructor(uint256 _initialValue) {
        storedData = _initialValue;
    }
    
    function set(uint256 _value) public {
        storedData = _value;
        emit DataStored(_value, msg.sender);
    }
    
    function get() public view returns (uint256) {
        return storedData;
    }
}
