"""Python project to create and display an experimental blockchain.

This project is primarily for the purpose of learning simple blockchain
programming and including Google Python style documentation. It creates
a proof of work function to mine out blocks containing UTF-8 encrypted data.
For security, it also includes a function to validate the blockchain
and return an error if invalid. The blockchain module exports to the main
module for use in the FastAPI localhost display.

"""
import datetime as _dt
import hashlib as _hashlib
import json as _json


class Blockchain:
    """Takes input information and encrypts it through proof of work mining.

    The blockchain takes an input of data, and encodes it using the sha256
    equation. This encoded information is validated through a proof of work
    function in order to maintain security. Information validated into the
    chain cannot be edited once mined into the chain.

    """

    def __init__(self):
        """
        This function creates the first block with a hash of 0.

        """
        self.chain = list()
        initial_block = self._create_block(
            data="I am the Genesis Block", proof=1, previous_hash="0", index=1
        )
        self.chain.append(initial_block)

    def mine_block(self, data: str) -> dict:
        """
        This function mines new blocks into the chain.

        Mining blocks assigns a calculated hash to a given set of
        information. The function pulls the information of the previous blocks
        and uses it to submit the new block to the chain.

        Args:
            data: Information to encode within the block.

        Returns:
            block: Key data necessary for blockchain
                function, including block data, proof of work, previous hash,
                and block index.

        """
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self._proof_of_work(
            previous_proof=previous_proof, index=index, data=data
        )
        previous_hash = self._hash(block=previous_block)
        block = self._create_block(
            data=data, proof=proof, previous_hash=previous_hash, index=index
        )
        self.chain.append(block)
        return block

    def _create_block(
        self, data: str, proof: int, previous_hash: str, index: int
    ) -> dict:
        """
        Adds new blocks to the chain.

        This function gathers the information dictionary necessary to mine
        out a new block to the chain. The dataset generated here is taken from
        a validated new block and submitted as the official block on the chain.

        Args:
            data: Information to encode within a block.
            proof: Numerical value to help validate completion of hash
                encryption for each block.
            previous_hash: Prior output value of sha256 encoded data.
            index: Numerical position in the blockchain order.

        Returns:
            block: Key data for the block as registered on the chain.

        """
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash,
        }

        return block

    def get_previous_block(self) -> dict:
        """
        Pulls the previous block in the chain.

        """
        return self.chain[-1]

    def _to_digest(
        self, new_proof: int, previous_proof: int, index: int, data: str
    ) -> bytes:
        """
        Returns UTF-8 encoded version of the string.

        Args:
            new_proof: Proof value of the new block.
            previous_proof: Proof value of the previous block.
            index: Numerical position in blockchain order.
            data: Information to encode within a block.

        Returns:
            to_digest: Encoded output of block dataset.

        """
        to_digest = str(new_proof ** 2 - previous_proof ** 2 + index) + data
        return to_digest.encode()

    def _proof_of_work(
        self, previous_proof: str, index: int, data: str
    ) -> int:
        """
        Proves computational effort for validating each block.

        Args:
            previous_proof: Proof value of the previous block.
            index: Numerical position in blockchain order.
            data: Information to encode within a block.

        Returns:
            new_proof: Proof value of the new block.

        """
        new_proof = 1
        check_proof = False

        while not check_proof:
            to_digest = self._to_digest(new_proof, previous_proof, index, data)
            hash_operation = _hashlib.sha256(to_digest).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def _hash(self, block: dict) -> str:
        """
        Hashes a block and returns it's cryptographic hash.

        Args:
            block: Key data for the block as registered on the chain.

        Returns:
            encoded_block: Sha256 encoded hash value of the block.

        """
        encoded_block = _json.dumps(block, sort_keys=True).encode()

        return _hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self) -> bool:
        """
        Validates previous hash compared to current block.

        Returns:
            True when previous hash of current block equals
                hash of previous block.
            False when previous hash of current block does not equal
                hash of previous block.

        """
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]
            # Check if the previous hash of the current block is the same
            # as the hash of it's previous block
            if block["previous_hash"] != self._hash(previous_block):
                return False

            previous_proof = previous_block["proof"]
            index, data, proof = block["index"], block["data"], block["proof"]
            hash_operation = _hashlib.sha256(
                self._to_digest(
                    new_proof=proof,
                    previous_proof=previous_proof,
                    index=index,
                    data=data,
                )
            ).hexdigest()

            if hash_operation[:4] != "0000":
                return False

            previous_block = block
            block_index += 1

        return True
