pragma solidity ^0.5.0;
//  Import the following contracts from the OpenZeppelin library:
//    * `ERC20`
//    * `ERC20Detailed`
//    * `ERC20Mintable`
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Burnable.sol";
// Create a constructor for the DalmasCoin contract and have the contract inherit the libraries that you imported from OpenZeppelin.
contract DalmasToken is ERC20, ERC20Detailed, ERC20Mintable, ERC20Burnable {
    constructor(
        string memory name,
        string memory symbol,
        uint initial_supply
    )
        ERC20Mintable()
        ERC20Burnable()
        ERC20Detailed(name, symbol, 18)
        public
    {// mint(msg.sender, initial_supply);
    }

    
}