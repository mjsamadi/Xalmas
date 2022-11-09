# Imports
import os
import json
from time import time_ns
import requests
from eth_account import account
from eth_typing import abi
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
from crypto_wallet import generate_account, get_balance, send_transaction
from PIL import Image

from wallet_connect import wallet_connect

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
accounts = w3.eth.accounts
chain_id = 1337

nft_address_contract=os.getenv("SMART_CONTRACT_ADDRESS")

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
diamond_database=db_list

my_address = "0x6f4413d21ec0cBBF9Da8322ba7BDC16D17d62461"
private_key = "0xb7701451ad715d59abcafd0ff5b055989d2d7925fe06598f82abc6bcc0ce6fbc"

################################################################################
# Contract Helper functions:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################
@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/dealing.json')) as f:
        auction_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("AUCTION_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=auction_abi
    )
    
    return contract, contract_address

################################################################################
# Inro Page
################################################################################
def intro():
    import streamlit as st
    
    st.write("# Welcome to Xalmas Dealing Room!")
    st.sidebar.success("Select a use case from side bar")
    st.markdown(
        """
        ### We have following Diamond in Xalmas shop. All of our Diamond certifed by GIA, and keep them. 
    """
    )

    for number in diamonds:
      st.text("====================================================")
      st.image(db_list[number][4], width=300)
      st.write(" Diamond ID: ", db_list[number][0])
      st.write(" GIA Certificate ID: ", db_list[number][2])
      st.write(" Rapaport Price: ", db_list[number][3], "USD")
      st.write(" NFT Address: ", nft_address_contract)
      st.write(" NFT ID:", db_list[number][1] )
      st.text("====================================================")
      st.text(" \n")

################################################################################
# Dashboard Page
################################################################################
def dashboard():
    import streamlit as st

    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    st.write(
        """
        Current Auction status
        """
    )
    contract,contract_address = load_contract()
    start = contract.functions.started().call()
    st.markdown(f"### Acution Started: {start}")

    nft_address = contract.functions.nft().call()
    st.markdown(f"### NFT address in Acution: {nft_address}")

    nft_id = contract.functions.nftId().call()
    st.markdown(f"### NFT ID in Acution: {nft_id}")

    highestBid = contract.functions.highestBid().call()
    st.markdown(f"### Highest Bid Value: {highestBid}")

    highestBidder = contract.functions.highestBidder().call()
    st.markdown(f"### Highest Bidder: {highestBidder}")

    endAt = contract.functions.endAt().call()
    st.markdown(f"### Bid End Time: {endAt}")

################################################################################
# Start Acution Page
################################################################################
def start_auction():
    import streamlit as st

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        ### Choose one of the NFTs for start new Auction.
        """
    )

    contract,contract_address = load_contract()
    start = contract.functions.started().call()
    st.sidebar.write("Acution Started:", start)

    nft_address = contract.functions.nft().call()
    st.sidebar.write("NFT address in Acution:", nft_address)

    nft_id = contract.functions.nftId().call()
    st.sidebar.write("NFT ID in Acution:", nft_id)

    highestBid = contract.functions.highestBid().call()
    st.sidebar.write("Highest Bid Value:", highestBid)

    highestBidder = contract.functions.highestBidder().call()
    st.sidebar.write("Highest Bidder:", highestBidder)

    endAt = contract.functions.endAt().call()
    st.sidebar.write("Bid End Time:", endAt)


    st.markdown("Admin Account Address for start the Acution:")
    address = st.selectbox("Select Account", options=accounts)

    # Create a select box to chose a car to bid on
    diamond = str(st.selectbox('Select Diamond NFT', diamonds))

    # Identify the Art for auction
    diamond_name = diamond_database[diamond][0]
    nft_id = int(diamond_database[diamond][1])

    # Write the art's name to the sidebar
    st.write("#### NFT Name:")
    st.write(diamond_name)

    # Identify the the starting bid for the art being auctioned
    st.write("#### Rapaport value:")
    starting_bid = diamond_database[diamond][3]

    # Write the arts starting bid
    st.write(starting_bid, " USD")

    # Identify the auction owner's Ethereum Address
    st.write("#### NFT Address and ID: ")
    st.write(nft_address_contract, "/ ",nft_id)

    st.write("#### Starting Bid valus in USD:")

    ## Additional code apart from BID, to showcase proof of transaction
    purchase_price = int(starting_bid)

    # Write the `total purchase` calculation to the Streamlit sidebar
    st.write(purchase_price, " USD")

    if st.button("Start Auction"):
        tx_hash = contract.functions.start(
            nft_address_contract,
            nft_id,
            purchase_price            
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.sidebar.write("============================")
        st.sidebar.write("Transaction receipt mined:")
        st.sidebar.write(dict(receipt))
    return (nft_address, nft_id, starting_bid)

################################################################################
# Bid Page
################################################################################
def register_bid():
    import streamlit as st
    from datetime import datetime

    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    st.write(
        """
        Offer new price in bid
        """
    )
  
    contract,contract_address = load_contract()
    start = contract.functions.started().call()
    st.sidebar.write("Acution Started:", start)

    nft_address = contract.functions.nft().call()
    st.sidebar.write("NFT address in Acution:", nft_address)

    nft_id = contract.functions.nftId().call()
    st.sidebar.write("NFT ID in Acution:", nft_id)

    highestBid = contract.functions.highestBid().call()
    st.sidebar.write("Highest Bid Value:", highestBid)

    highestBidder = contract.functions.highestBidder().call()
    st.sidebar.write("Highest Bidder:", highestBidder)

    endAt = contract.functions.endAt().call()
    st.sidebar.write("Bid End Time:", endAt)
    # st.sidebar.write("Remian Time for Bid:", datetime.utcnow())

    st.markdown("User Account Address for bid the Acution:")
    st.markdown(my_address)

    # Identify the Art for auction
    diamond = pool[nft_id]
    # Write the art's name to the sidebar
    st.write("#### NFT Name:")
    st.write(diamond)

    # Identify the the starting bid for the art being auctioned
    st.write("#### Rapaport value:")
    starting_bid = diamond_database[diamond][3]
    # Write the arts starting bid
    st.write(starting_bid, " USD")

    new_price = st.text_input("Enter the new price (USD)")
    
    wallet_button = wallet_connect(label="wallet", key="wallet")
    st.write(f"Wallet {wallet_button} connected.")

    if st.button("Register offer"):
        nonce = w3.eth.getTransactionCount(my_address)
        bid_transaction =contract.functions.bid().buildTransaction(
            {
            "from": my_address,
            "gas": 1000000,
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "nonce": nonce,
            "value": int(new_price)
        }
        )
        signed_tx = w3.eth.account.signTransaction(bid_transaction, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        st.sidebar.write(dict(tx_receipt))

###
#    if st.button("Bid3"):
#        chain_id = 1337
#        my_address = "0x6f4413d21ec0cBBF9Da8322ba7BDC16D17d62461"
#        private_key = "0xb7701451ad715d59abcafd0ff5b055989d2d7925fe06598f82abc6bcc0ce6fbc"
#        nonce = w3.eth.getTransactionCount(my_address)
#        send_transaction = wallet_connect(label="send", key="send", message="Send Transaction", contract_address="", amount="10", to_address=address)
#        st.sidebar.write(send_transaction)
###
################################################################################
# End Auction Page
################################################################################
def end_auction():
    import streamlit as st

    st.markdown(f"# {list(page_names_to_funcs.keys())[4]}")
    st.write(
        """
        End Auction
        """
    )
    
    contract,contract_address = load_contract()
    start = contract.functions.started().call()
    st.sidebar.write("Acution Started:", start)

    nft_address = contract.functions.nft().call()
    st.sidebar.write("NFT address in Acution:", nft_address)

    nft_id = contract.functions.nftId().call()
    st.sidebar.write("NFT ID in Acution:", nft_id)

    highestBid = contract.functions.highestBid().call()
    st.sidebar.write("Highest Bid Value:", highestBid)

    highestBidder = contract.functions.highestBidder().call()
    st.sidebar.write("Highest Bidder:", highestBidder)

    endAt = contract.functions.endAt().call()
    st.sidebar.write("Bid End Time:", endAt)
    # st.sidebar.write("Remian Time for Bid:", datetime.utcnow())

    st.markdown("Admin Account Address for start the Acution:")
    address = st.selectbox("Select Account", options=accounts)
    
    if st.button("End Auction"):
        tx_hash = contract.functions.end().transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.sidebar.write("============================")
        st.sidebar.write("End Transaction receipt:")
        st.sidebar.write(dict(receipt))
        st.balloons()
        st.write("# Winner:", highestBidder)

################################################################################
# Withdraw Page
################################################################################
def withdraw():
    import streamlit as st
    import pandas as pd
    import altair as alt

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[5]}")
    st.write(
        """
        Withdraw
        """
    )
    contract,contract_address = load_contract()
    start = contract.functions.started().call()
    st.sidebar.write("Acution Started:", start)

    nft_address = contract.functions.nft().call()
    st.sidebar.write("NFT address in Acution:", nft_address)

    nft_id = contract.functions.nftId().call()
    st.sidebar.write("NFT ID in Acution:", nft_id)

    highestBid = contract.functions.highestBid().call()
    st.sidebar.write("Highest Bid Value:", highestBid)

    highestBidder = contract.functions.highestBidder().call()
    st.sidebar.write("Highest Bidder:", highestBidder)

    endAt = contract.functions.endAt().call()
    st.sidebar.write("Bid End Time:", endAt)
    # st.sidebar.write("Remian Time for Bid:", datetime.utcnow())

    st.markdown("Admin Account Address for withdraw")
    address = st.selectbox("Select Account", options=accounts)

    if st.button("Withdraw"):
        tx_hash = contract.functions.withdraw().transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.sidebar.write("============================")
        st.sidebar.write("Withdraw Transaction receipt:")
        st.sidebar.write(dict(receipt))

################################################################################
################################################################################
# Streamline Code
################################################################################
################################################################################

page_names_to_funcs = {
    "Home": intro,
    "Auction Dashboard": dashboard,
    "Start Auction (Admin)": start_auction,
    "Offer New Price": register_bid,
    "End Aution (Admin)": end_auction,
    "Offer Withdraw": withdraw
}

image = Image.open('./Images/diamond.jpg')

st.image(image, caption='Xalmas')

acution_contract, contract_address = load_contract()
st.sidebar.write("Auction Contract Address: ",contract_address)

usecase = st.sidebar.selectbox("Choose a function", page_names_to_funcs.keys())
page_names_to_funcs[usecase]()




