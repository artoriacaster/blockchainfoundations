"""Python project to create and display an experimental blockchain.

This project is primarily for the purpose of learning simple blockchain
programming and including Google Python style documentation. The Blockchain
module creates a proof of work function to mine out blocks containing UTF-8
encrypted data. For security, it also includes a function to validate the
blockchain and return an error if invalid. The main module imports the
blockchain module for use in a FastAPI localhost display.

"""

import fastapi as _fastapi
import blockchain as _blockchain

blockchain = _blockchain.Blockchain()
app = _fastapi.FastAPI()


# FastAPI endpoint to mine out a block.
# Returns error if the blockchain is not valid.
@app.post("/mine_block/")
def mine_block(data: str):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(
                status_code=400, detail="The blockchain is invalid")
    block = blockchain.mine_block(data=data)

    return block


# FastAPI endpoint to return the blockchain.
# Returns error if the blockchain is not valid.
@app.get("/blockchain/")
def get_blockchain():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid")
    chain = blockchain.chain
    return chain


# FastAPI endpoint to see chain validity.
# Returns error if the blockchain is not valid.
@app.get("/validate/")
def is_blockchain_valid():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid")

    return blockchain.is_chain_valid()


# FastAPI endpoint to return data of previous block.
# Returns error if the blockchain is not valid.
@app.get("/blockchain/previous/")
def previous_block():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid")

    return blockchain.get_previous_block()
