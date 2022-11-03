pragma solidity ^0.5.0;

import "./DalmasCoin.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";


// Have the DalmasCoinCrowdsale contract inherit the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale
contract DalmasCoinCrowdsale is Crowdsale, MintedCrowdsale { 
    constructor(
        uint256 rate,
        address payable wallet,
        DalmasCoin token
    ) public Crowdsale(rate, wallet, token) {
        // constructor can stay empty
    }
}


contract DalmasCoinCrowdsaleDeployer {
    // Create an `address public` variable called `Dalmas_token_address`.
    address public Dalmas_token_address;
    // Create an `address public` variable called `Dalmas_crowdsale_address`.
    address public Dalmas_crowdsale_address;

    // Add the constructor.
    constructor(
       string memory name,
        string memory symbol,
        address payable wallet
    ) public {
        // Create a new instance of the DalmasCoin contract.
        DalmasCoin token = new DalmasCoin (name, symbol, 0);
        
        // Assign the token contract’s address to the `Dalmas_token_address` variable.
        Dalmas_token_address = address(token);

        // Create a new instance of the `DalmasCoinCrowdsale` contract
        DalmasCoinCrowdsale  DalmasCoin_crowdsale =
            new DalmasCoinCrowdsale(1, wallet, token);
            
        // Aassign the `DalmasCoinCrowdsale` contract’s address to the `Dalmas_crowdsale_address` variable.
        Dalmas_crowdsale_address = address(DalmasCoin_crowdsale);

        // Set the `DalmasCoinCrowdsale` contract as a minter
        token.addMinter(Dalmas_crowdsale_address);
        
        // Have the `DalmasCoinCrowdsaleDeployer` renounce its minter role.
        token.renounceMinter();
    }
}
