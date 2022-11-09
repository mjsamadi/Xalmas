# Imports
import os
import json
import requests
from eth_account import account
from eth_typing import abi
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
# from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
from PIL import Image

##from crypto_wallet import generate_account, get_balance, send_transaction
load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
accounts = w3.eth.accounts

auctions=os.getenv("AUCTION_CONTRACT_ADDRESS")
auctions=[auctions, "NA"]

url=os.getenv("DB_URL")

# Diamond Database
#diamond_database = {
#         "Diamond1": ["Diamond1", "0", "2141438167", 6750, "https://gateway.pinata.cloud/ipfs/QmUqCEaURthbSNB9JLjbhMpfTDqyfsyob6RH5pwsSgqxTk/image1.png"],
#         "Diamond2": ["Diamond2", "1", "6271461533", 2480, "https://gateway.pinata.cloud/ipfs/QmUqCEaURthbSNB9JLjbhMpfTDqyfsyob6RH5pwsSgqxTk/image2.png"],
#         "Diamond3": ["Diamond3", "2", "55245801", 8140, "https://gateway.pinata.cloud/ipfs/QmUqCEaURthbSNB9JLjbhMpfTDqyfsyob6RH5pwsSgqxTk/image3.png"],
#         "Diamond4": ["Diamond4", "3", "22077474081", 8340, "https://gateway.pinata.cloud/ipfs/QmUqCEaURthbSNB9JLjbhMpfTDqyfsyob6RH5pwsSgqxTk/Image4.png"],
#         "Diamond5": ["Diamond5", "4", "2151153863", 4650, "https://gateway.pinata.cloud/ipfs/QmUqCEaURthbSNB9JLjbhMpfTDqyfsyob6RH5pwsSgqxTk/Image5.jpg"],
#         "Diamond6": ["Diamond6", "5", "1187080939", 5140, "https://gateway.pinata.cloud/ipfs/QmUqCEaURthbSNB9JLjbhMpfTDqyfsyob6RH5pwsSgqxTk/Image6.jpg"],
#         "Diamond7": ["Diamond7", "6", "2145936424", 7410, "https://gateway.pinata.cloud/ipfs/QmUqCEaURthbSNB9JLjbhMpfTDqyfsyob6RH5pwsSgqxTk/Image7.jpg"]
#         }

diamonds = ["Diamond1", "Diamond2", "Diamond3", "Diamond4", "Diamond5", "Diamond6", "Diamond7"]
pool = diamonds
db_list = json.loads(requests.get(url).text)

################################################################################
# Contract Helper functions:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################
@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/XalmasRegistry.json')) as f:
        auction_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=auction_abi
    )
    
    return contract, contract_address

################################################################################
# Intro Page
################################################################################
def intro():
    import streamlit as st
    
    st.write("# Welcome to Xalmas Showroom!")
    st.markdown(
        """
        !!!!!!
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        !!!!!
    """
    )
    
################################################################################
# Diamond Pool
################################################################################
def listing():
    import streamlit as st

    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    st.write(
        """
        Diamond Pool
        """
    )

    for number in diamonds:
      st.text("====================================================")
      st.image(db_list[number][4], width=300)
      st.write(" Diamond ID: ", db_list[number][0])
      st.write(" GIA Certificate ID: ", db_list[number][2])
      st.write(" Rapaport Price: ", db_list[number][3], "USD")
      st.text("====================================================")
      st.text(" \n")

################################################################################
# Mint Diamond NFT
################################################################################
def mint_nft():
    import streamlit as st

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
       
    st.markdown("## Register GIA Certification")
    address = st.selectbox("Select Account as Owner and Minter of Diamond NFT", options=accounts)
    diamond_name = st.selectbox("Select from Diamond Pool", options = pool)
    giaid= db_list[diamond_name][2]
    value= int(db_list[diamond_name][3])
    uri= db_list[diamond_name][4]
    
    st.text("====================================================")
    st.image(db_list[diamond_name][4], width=300)
    st.write(" Diamond ID: ", db_list[diamond_name][0])
    st.write(" GIA Certificate ID: ", db_list[diamond_name][2])
    st.write(" Rapaport Price: ", db_list[diamond_name][3], "USD")
    st.text("====================================================")
    st.text(" \n")

    contract, contract_address = load_contract()
    st.sidebar.write("Auction Contract Address: ",contract_address)

    if st.button("Register Xalmas NFT"):
        tx_hash = contract.functions.registerNFT(
            address,
            diamond_name,
            giaid,
            value,
            uri
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.sidebar.write("Transaction receipt mined:")
        st.sidebar.write(dict(receipt))

################################################################################
# Diamond Value
################################################################################
def diamond_value():
    import streamlit as st

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        Diamond Value
        """
    )
    
    st.markdown("## Update Diamond value")
    address = st.selectbox("Select Account as Owner of Diamond NFT", options=accounts)
    diamond_name = st.selectbox("Select from Diamond Pool", options = pool)

    contract, contract_address = load_contract()
    st.sidebar.write("Auction Contract Address: ",contract_address)

    st.text("====================================================")
    st.image(db_list[diamond_name][4], width=300)
    st.write(" Diamond ID: ", db_list[diamond_name][0])
    st.write(" GIA Certificate ID: ", db_list[diamond_name][2])
    st.write(" Rapaport Price: ", db_list[diamond_name][3], "USD")
    st.write(" NFT Address: ", contract_address)
    st.write(" TokenID: ", db_list[diamond_name][1])
    st.text("====================================================")
    st.text(" \n")

    tokenId= int(db_list[diamond_name][1])
    newValue = st.text_input("Enter the new Value for Diamond")
    reportUri = st.text_input("Enter the Report URI")

    if st.button("Update Xalmas Value"):
        tx_hash = contract.functions.newAppraisal(
            tokenId,
            int(newValue),
            reportUri
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.sidebar.write("Transaction receipt mined:")
        st.sidebar.write(dict(receipt))

################################################################################
# Send to Auction
################################################################################
def send_to_auction():
    import streamlit as st

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        Send Diamond NFT to Auction
        """
    )
    
    st.markdown("## Send a Dinamond NFT for Auction")
    address = st.selectbox("Select Account as Owner of Diamond NFT", options=accounts)
    diamond_name = st.selectbox("Select from Diamond Pool", options = pool)

    contract, contract_address = load_contract()
    st.sidebar.write("Auction Contract Address: ",contract_address)

    st.text("====================================================")
    st.image(db_list[diamond_name][4], width=300)
    st.write(" Diamond ID: ", db_list[diamond_name][0])
    st.write(" GIA Certificate ID: ", db_list[diamond_name][2])
    st.write(" Rapaport Price: ", db_list[diamond_name][3], "USD")
    st.write(" NFT Address: ", contract_address)
    st.write(" TokenID: ", db_list[diamond_name][1])
    st.text("====================================================")
    st.text(" \n")

    tokenId= int(db_list[diamond_name][1])

    acution_address = st.selectbox("Select Auction address", options=auctions)

    if st.button("Send to Auction"):
        tx_hash = contract.functions.approve(
            acution_address,
            tokenId
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.sidebar.write("Transaction receipt mined:")
        st.sidebar.write(dict(receipt))

################################################################################
################################################################################
# Streamline Code
################################################################################
################################################################################

page_names_to_funcs = {
    "Home": intro,
    "Diamond Pool": listing,
    "Mint Diamond NFT": mint_nft,
    "Update Diamond Value": diamond_value,
    "Send to Auction": send_to_auction    
}

usecase = st.sidebar.selectbox("Choose a function", page_names_to_funcs.keys())
page_names_to_funcs[usecase]()

# Load the contract
contract, contract_address = load_contract()
