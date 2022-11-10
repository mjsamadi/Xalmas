pragma solidity ^0.5.0;

import "./DalmasToken.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/CappedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/TimedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/distribution/RefundablePostDeliveryCrowdsale.sol";

// Have the DalmasCoinCrowdsale contract inherit the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale
contract DalmasTokenCrowdsale is Crowdsale, MintedCrowdsale, CappedCrowdsale, TimedCrowdsale, RefundableCrowdsale{ 
    constructor(
        uint256 rate,
        address payable wallet,
        DalmasToken token,
        uint goal, // the crowdsale goal
        uint open, // the crowdsale opening time
        uint close // the crowdsale closing time
    ) public 
        Crowdsale(rate, wallet, token)
        MintedCrowdsale()
        CappedCrowdsale(goal)
        TimedCrowdsale(open, close)
        RefundableCrowdsale(goal)

    {
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
        address payable wallet,
        uint goal // the crowdsale goal
    
    ) public {
        // Create a new instance of the DalmasCoin contract.
        DalmasToken token = new DalmasToken (name, symbol, 0);
        
        // Assign the token contract’s address to the `Dalmas_token_address` variable.
        Dalmas_token_address = address(token);

        // Create a new instance of the `DalmasCoinCrowdsale` contract
        DalmasTokenCrowdsale  DalmasToken_crowdsale =
            new DalmasTokenCrowdsale(1, wallet, token, goal, now, now + 24 weeks);
            
        // Aassign the `DalmasCoinCrowdsale` contract’s address to the `Dalmas_crowdsale_address` variable.
        Dalmas_crowdsale_address = address(DalmasToken_crowdsale);

        // Set the `DalmasCoinCrowdsale` contract as a minter
        token.addMinter(Dalmas_crowdsale_address);
        token.addMinter(Dalmas_token_address);
        token.addMinter(msg.sender);
        // Have the `DalmasCoinCrowdsaleDeployer` renounce its minter role.
        //token.renounceMinter();
        
    }
}