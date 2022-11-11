# Imports
import json
import math
from dataclasses import dataclass
from typing import Any, List
import streamlit as st
from streamlit_player import st_player
from investor_wallet import generate_account, get_balance
from bip44 import Wallet
from web3 import Account, Web3
from dotenv import load_dotenv
from web3.gas_strategies.time_based import medium_gas_price_strategy





#----------------------------------------------------------------------------------------------------------------------
# Preparations 
#----------------------------------------------------------------------------------------------------------------------

# Link app with ganache
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# Load all abi files

with open("C:/Users/dude/Downloads/DalmasToken_abi.json") as token_abi:
        DalmasToken_abi = json.load(token_abi)
with open("C:/Users/dude/Downloads/DalmasTokenCrowdsale_abi.json") as crowdsale_abi:
        DalmasTokenCrowdsale_abi = json.load(crowdsale_abi)
with open("C:/Users/dude/Downloads/DalmasTokenCrowdsaleDeployer_abi.json") as deployer_abi:
        DalmasTokenCrowdsaleDeployer_abi = json.load(deployer_abi)

# Establish Dalmas database
Dalmas_database = {
    "Dalmas": ["Dalmas", '0x69922885a3FC7E8693E8a9f7cF0a71708543E2Fd', 0.1, "C:/Users/dude/Downloads/daimond.jpg",
    '0xcddF785d0382B8e9b8b7D1c4b13422E8B8aCB44D', '0xC07985A48927C6b39C5BE65aA323840C1C5D5430', DalmasTokenCrowdsaleDeployer_abi, DalmasTokenCrowdsale_abi, DalmasToken_abi]
}
#db_list = list(Dalmas_database.values())

# A list of Daimond token names
token_name = ["Dalmas"]
investor_account = generate_account()
#

#
################################################################################
# Buy token Page
###############################################################################

def Buy_Dalmas():
    import streamlit as st
    import pandas as pd
    import altair as alt

    from urllib.error import URLError
    token_name = ["Dalmas"]
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    st.write(
        """
        
        """
    )
    st.markdown("## Purchase Dalmas Tokens HERE!")
    st.image('daimond_2.jpg', width= 400)
    # Allow investors to create an account to buy tokens
    #investor_account = generate_account()

    # Write investor Ethereum account address and ballance 
    st.markdown("## My account")
    st.write(investor_account.address)
    st.write(get_balance(w3, investor_account.address), "ETH")

    #Allow investors to select tokens to invest
    token_name = st.selectbox('Select Token to Invest', token_name)

    number_of_tokens = st.number_input("Number of Tokens Purchasing", step = 1)

    #st.write('---')
    #st.markdown("## Token Name ##")
    
    # Identify the token name that investing to
    #dalmas = Dalmas_database[token_name][0]

    # Write the token name to 
    #st.write(dalmas)

    # Clarify token price
    st.markdown("## Token Price ##")
    token_price = Dalmas_database[token_name][2]

    # Write the token price 
    st.write(token_price)

    # Identify  Ethereum Address
    #st.markdown("## CrowdSal Address ##")
    #dalmas_address = Dalmas_database[token_name][4]

    # Write selected dalmas Ethereum Address 
    #st.write(dalmas_address)

    # Write total cost of tokens
    st.markdown("## Total Token Cost in Ether")
    total_cost = token_price * number_of_tokens
    st.write(total_cost)

    #st.write(dalmas_address)
    #st.write(investor_account)

    # Load deployer, crowdsale, and token contracts with abi files
    deployer_contract=w3.eth.contract(address=Dalmas_database[token_name][1], abi=Dalmas_database[token_name][6])
    crowdsale_contract=w3.eth.contract(address=Dalmas_database[token_name][4], abi=Dalmas_database[token_name][7])
    token_contract=w3.eth.contract(address=Dalmas_database[token_name][5], abi=Dalmas_database[token_name][8])

    
    def write_supply():
        # Get how many tokens are left in crowdsale
         #   cap_goal = crowdsale_contract.functions.cap().call() * 10 ** (-18)
        total_raised = crowdsale_contract.functions.weiRaised().call() 
        token_raised = total_raised / 100000000000000000
         # Calculate remaining number of tokens available for sale
        total_supply = token_contract.functions.totalSupply().call()
        # cap = crowdsale_contract.functions.cap().call()
        # remaining_tokens = cap - total_supply
         #   supply_left = total_supply - total_raised
        symbol = token_contract.functions.name().call()
        my_token_Balance = token_contract.functions.balanceOf(investor_account.address).call()
        my_tokens_Balance = my_token_Balance / 100000000000000000
        # Display total tokens left in crowdsale
        st.markdown("## My Tokens")
        st.write(f"{my_tokens_Balance} Tokens")
        st.write(f"{symbol} Tokens")
        st.markdown("## Tokens Raised")
        st.write(f"{token_raised} Tokens")
        st.write(f"{symbol} Tokens")
        
   
#----------------------------------------------------------------------------------------------------------------------
# Transaction functionality designs
#----------------------------------------------------------------------------------------------------------------------
    def buy_token(w3, beneficiary, total_price):
        """Send an authorized transaction."""
        chain_id = 1337
        my_address = "0xE10322bebFb7B382ad21e19B5c7F9743A9654Fe2"
        private_key = "3a6a21605df79d063581e7807d7643a54413f751e2d8b7e479c985b1559abb12"
        nonce = w3.eth.getTransactionCount(my_address)
        wei_value = w3.toWei(total_price, "ether")

        buy_transaction =crowdsale_contract.functions.buyTokens(my_address).buildTransaction(
            {
            "from": my_address,
            "gas": 2000000,
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "nonce": nonce,
            "value": wei_value
        }
        )
        signed_tx = w3.eth.account.signTransaction(buy_transaction, private_key=private_key)
        return w3.eth.send_raw_transaction(signed_tx.rawTransaction)


    # Click button to buy tokens
    if st.button("Buy Token"):

        transaction_hash = buy_token(w3,investor_account, total_cost)
        tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
        write_supply()
        # Markdown for the transaction hash
        st.markdown("#### Validated Transaction Hash")

        # Write the returned transaction hash to the screen
        st.write(transaction_hash)
        # Markdown for the transaction hash
        st.markdown("#### Validated Transaction Receipt")

        # Write the returned transaction hash to the screen
        st.write(dict(tx_receipt))
        
        # Celebrate your successful payment
        st.balloons

################################################################################
# Refund Dalmas Page
###############################################################################

def Refund_Dalmas():
    import streamlit as st
    import pandas as pd
    import altair as alt

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    st.write(
        """
        Refund Dalmas
        """
    )
    
    # Load deployer, crowdsale, and token contracts with abi files
    token_name = ["Dalmas"]
    token_name = st.selectbox('Select Token to refund', token_name)
    dalmas_amount = st.number_input("Number of Tokens to refund", step = 1)
    deployer_contract=w3.eth.contract(address=Dalmas_database[token_name][1], abi=Dalmas_database[token_name][6])
    crowdsale_contract=w3.eth.contract(address=Dalmas_database[token_name][4], abi=Dalmas_database[token_name][7])
    token_contract=w3.eth.contract(address=Dalmas_database[token_name][5], abi=Dalmas_database[token_name][8])
    
    def refund_token(w3, token_amount) :
        chain_id = 1337
        my_address = "0x4d53C070604b656232b0E813A415F7077904497d"
        private_key = "30c46d7703b7fc15c84d295f2f360b21d02f1c1cb65988c7520db992666284a8"
        nonce = w3.eth.getTransactionCount(my_address)
        wei_value = token_amount
        refund_transaction =crowdsale_contract.functions.claimRefund(my_address).buildTransaction(
            {
            "from": my_address,
            "gas": 2000000,
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "nonce": nonce,
            "value": 0
            }
            )
        signed_tx = w3.eth.account.signTransaction(refund_transaction, private_key=private_key)
        return w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Click button to mint tokens
    if st.button("refund Dalmas"):

        transaction_hash = refund_token(w3, dalmas_amount)
        tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

        # Markdown for the transaction hash
        st.markdown("#### Validated Transaction Hash")

        # Write the returned transaction hash to the screen
        st.write(transaction_hash)
        write_supply()
        
        # Markdown for the transaction hash
        st.markdown("#### Validated Transaction Receipt")

        # Write the returned transaction hash to the screen
        st.write(dict(tx_receipt))

        # Celebrate your successful payment
        st.balloons()
    
    
    
    
    
#################################################################################

# Dashboard Dalmas Page
###############################################################################

def Dashboard():
    import streamlit as st
    import pandas as pd
    import altair as alt
    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[0]}")
    st.write("## Shine Like a Daimon")
    st.video('https://www.youtube.com/watch?v=lWA2pjMjpBs')
    token_name = ["Dalmas"]
    token_name = st.selectbox('Token Name', token_name)
    deployer_contract=w3.eth.contract(address=Dalmas_database[token_name][1], abi=Dalmas_database[token_name][6])
    crowdsale_contract=w3.eth.contract(address=Dalmas_database[token_name][4], abi=Dalmas_database[token_name][7])
    token_contract=w3.eth.contract(address=Dalmas_database[token_name][5], abi=Dalmas_database[token_name][8])
    def write_supply():
         ##Get how many tokens are left in crowdsale
        #cap_goal = crowdsale_contract.functions.cap().call() * 10 ** (-18)
        total_raised = crowdsale_contract.functions.weiRaised().call()
        token_raised = total_raised / 100000000000000000
         # Calculate remaining number of tokens available for sale
        total_supply = token_contract.functions.totalSupply().call()
        token_supply = total_supply / 100000000000000000
        cap = crowdsale_contract.functions.cap().call()
        cap_Token = cap / 100000000000000000
        remaining_tokens = cap_Token - token_supply
         #   supply_left = total_supply - total_raised
        symbol = token_contract.functions.name().call()
        # Display total tokens left in crowdsale
        st.markdown("## Tokens Supply")
        st.write(f"{token_supply} Tokens")
        st.markdown("## Tokens Raised")
        st.write(f"{token_raised} Tokens")
        st.markdown("## Tokens CAP")
        st.write(f"{cap_Token} Tokens")
        st.markdown("## Supply Left")
        st.write(f"{remaining_tokens} Tokens")
   
    
        
    write_supply()
    
    
    
    
    
    

#################################################################################

# Mint New Dalmas Page
###############################################################################

def Mint_Dalmas() :
    
    import streamlit as st
    import pandas as pd
    import altair as alt
    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        Mint Dalmas
        """
    )

   # Load deployer, crowdsale, and token contracts with abi files
    token_contract_address="0x34A4Ce2B6Bfa27eB360799c4776656d00D613370"
    token_name = ["Dalmas"]
    token_name = st.selectbox('Select Token to Invest', token_name)
    dalmas_amount = st.number_input("Number of Tokens to mint", step = 1)
    deployer_contract=w3.eth.contract(address=Dalmas_database[token_name][1], abi=Dalmas_database[token_name][6])
    crowdsale_contract=w3.eth.contract(address=Dalmas_database[token_name][4], abi=Dalmas_database[token_name][7])
    token_contract=w3.eth.contract(address=Dalmas_database[token_name][5], abi=Dalmas_database[token_name][8])
    def write_supply():
         ##Get how many tokens are left in crowdsale
        cap_goal = crowdsale_contract.functions.cap().call() * 10 ** (-18)
        total_raised = crowdsale_contract.functions.weiRaised().call() 
         # Calculate remaining number of tokens available for sale
        total_supply = token_contract.functions.totalSupply().call()
        total__token_supply= total_supply/100000000000000000
        # cap = crowdsale_contract.functions.cap().call()
        # remaining_tokens = cap - total_supply
         #   supply_left = total_supply - total_raised
        symbol = token_contract.functions.name().call()
        # Display total tokens left in crowdsale
        st.markdown("## Tokens Supply")
        st.write(f"{total__token_supply} Tokens")
        st.markdown("## Tokens CAP")
        st.write(f"{cap_goal} Tokens")
    
    def Mint_token(w3, token_amount) :
        chain_id = 1337
        my_address = "0xE1359162676D78992644c1AC6F43384869d935f3"
        private_key = "fd8cd0c61adc4a2f950b6a468b2cd29c37ee16c5f16917dbf32974d54fbdec23"
        nonce = w3.eth.getTransactionCount(my_address)
        wei_value = token_amount*100000000000000000
        Mint_transaction =token_contract.functions.mint(my_address, wei_value).buildTransaction(
            {
            "from": my_address,
            "gas": 2000000,
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "nonce": nonce,
            "value": 0
            }
            )
        signed_tx = w3.eth.account.signTransaction(Mint_transaction, private_key=private_key)
        return w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Click button to mint tokens
    if st.button("Mint Dalmas"):

        transaction_hash = Mint_token(w3, dalmas_amount)
        tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

        # Markdown for the transaction hash
        st.markdown("#### Validated Transaction Hash")

        # Write the returned transaction hash to the screen
        st.write(transaction_hash)
        write_supply()
        
        # Markdown for the transaction hash
        st.markdown("#### Validated Transaction Receipt")

        # Write the returned transaction hash to the screen
        st.write(dict(tx_receipt))

        # Celebrate your successful payment
        st.balloons()
    


#################################################################################

# Burn Dalmas Page
###############################################################################
def Burn_Dalmas():
    import streamlit as st
    import streamlit as st
    import pandas as pd
    import altair as alt

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[4]}")
    st.write(
        """
        Burn Dalmas
        """
    )
    # Load deployer, crowdsale, and token contracts with abi files
    token_contract_address="0x34A4Ce2B6Bfa27eB360799c4776656d00D613370"
    token_name = ["Dalmas"]
    token_name = st.selectbox('Select Token to burn', token_name)
    dalmas_amount = st.number_input("Number of Tokens to burn", step = 1)
    deployer_contract=w3.eth.contract(address=Dalmas_database[token_name][1], abi=Dalmas_database[token_name][6])
    crowdsale_contract=w3.eth.contract(address=Dalmas_database[token_name][4], abi=Dalmas_database[token_name][7])
    token_contract=w3.eth.contract(address=token_contract_address, abi=Dalmas_database[token_name][8])
    accounts = w3.eth.accounts
    account = accounts[1]
    my_address = "0xE1359162676D78992644c1AC6F43384869d935f3"
    def burn_token(w3, token_amount) :
        chain_id = 1337
        my_address = "0xE1359162676D78992644c1AC6F43384869d935f3"
        private_key = "fd8cd0c61adc4a2f950b6a468b2cd29c37ee16c5f16917dbf32974d54fbdec23"
        nonce = w3.eth.getTransactionCount(my_address)
        wei_value = token_amount*100000000000000000

        burn_transaction =token_contract.functions.burn(wei_value).buildTransaction(
          {
          "from": my_address,
          "gas": 2000000,
          "gasPrice": w3.eth.gas_price,
          "chainId": chain_id,
          "nonce": nonce,
          "value": 0
            }
            )
        signed_tx = w3.eth.account.signTransaction(burn_transaction, private_key=private_key)

        return w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Click button to mint tokens
    if st.button("Burn Dalmas"):

        transaction_hash = burn_token(w3, dalmas_amount)
        tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

        # Markdown for the transaction hash
        st.markdown("#### Validated Transaction Hash")

        # Write the returned transaction hash to the screen
        st.write(transaction_hash)
        write_supply()
        
        # Markdown for the transaction hash
        st.markdown("#### Validated Transaction Receipt")

        # Write the returned transaction hash to the screen
        st.write(dict(tx_receipt))

        # Celebrate your successful payment
        st.balloons()
 

#########################################################################
# page lisT
#########################################################################

page_names_to_funcs = {
    "DALMAS Dashboard": Dashboard ,
    "Buy Dalmas": Buy_Dalmas,
    "Mint new Dalmas": Mint_Dalmas ,
    "Refund Dalmas": Refund_Dalmas,
    "Burn Dalmas ":  Burn_Dalmas,
}

usecase = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[usecase]()

# Load the contract
#contract = load_contract()


