pragma solidity ^0.5.0;

import "./DalmasToken.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";


// Have the DalmasTokanCrowdsale contract inherit the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale
contract DalmasTokenCrowdsale is Crowdsale, MintedCrowdsale { 
    constructor(
        uint256 rate,
        address payable wallet,
        DalmasToken token
    ) public Crowdsale(rate, wallet, token) {
        // constructor can stay empty
    }
}


contract DalmasTokenCrowdsaleDeployer {
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
        // Create a new instance of the DalmasToken contract.
        DalmasToken token = new DalmasToken (name, symbol, 0);
        
        // Assign the token contract’s address to the `kasei_token_address` variable.
        Dalmas_token_address = address(token);

        // Create a new instance of the `DalmasTokenCrowdsale` contract
        DalmasTokenCrowdsale  DalmasToken_crowdsale = new DalmasTokenCrowdsale(1, wallet, token);
            
        // Aassign the `DalmasTokenCrowdsale` contract’s address to the `Dalmas_crowdsale_address` variable.
        Dalmas_crowdsale_address = address(DalmasToken_crowdsale);

        // Set the `DalmasTokenCrowdsale` contract as a minter
        token.addMinter(Dalmas_crowdsale_address);
        
        // Have the `DalmasTokenCrowdsaleDeployer` renounce its minter role.
        token.renounceMinter();
    }
}