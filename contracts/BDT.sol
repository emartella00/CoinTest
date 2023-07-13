// contracts/BDToken.sol
// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

import "OpenZeppelin/openzeppelin-contracts@4.9.0/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.9.0/contracts/token/ERC20/extensions/ERC20Burnable.sol";

contract BDT is ERC20Burnable {
    constructor(uint256 initialSupply) ERC20("BToken", "BDT") {
        _mint(msg.sender, initialSupply);
    }


}