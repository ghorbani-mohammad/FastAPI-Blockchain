import time
import hashlib


class MGHBlockchain:
    # Hypothetical blockchain for MGH coin
    def __init__(
        self, previous_block_hash, transaction_list, nonce=0, miner_address=None
    ):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list
        self.nonce = nonce
        self.miner_address = miner_address
        self.timestamp = time.time()

        self.block_data = (
            " | ".join(transaction_list)
            + " | "
            + previous_block_hash
            + " | "
            + str(nonce)
        )
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()


class BlockchainManager:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 2  # Number of leading zeros required
        self.mining_reward = 1  # MGH coins for mining a block

        # Hard-coded limits
        self.MAX_TRANSACTIONS_PER_BLOCK = 3
        self.MIN_TRANSACTIONS_PER_BLOCK = 1

        # Create genesis block
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = MGHBlockchain(
            "Genesis Block", ["Genesis Transaction"], 0, "Genesis"
        )
        self.chain.append(genesis_block)

    def add_transaction(self, transaction: str) -> dict:
        """Add transaction to pending pool"""
        if len(self.pending_transactions) >= self.MAX_TRANSACTIONS_PER_BLOCK:
            return {
                "status": "error",
                "message": "Transaction pool is full. Mine a block first.",
            }

        self.pending_transactions.append(transaction)
        return {
            "status": "success",
            "message": f"Transaction added. Pending: {len(self.pending_transactions)}",
        }

    def mine_block(self, miner_address: str) -> dict:
        """Mine a new block - any miner can call this"""
        if len(self.pending_transactions) < self.MIN_TRANSACTIONS_PER_BLOCK:
            return {
                "status": "error",
                "message": f"Need at least {self.MIN_TRANSACTIONS_PER_BLOCK} transactions to mine",
            }

        # Get previous block hash
        previous_hash = self.chain[-1].block_hash

        # Start mining with nonce
        nonce = 0
        max_attempts = 100000  # Prevent infinite loops

        while nonce < max_attempts:
            # Create block with current nonce
            block = MGHBlockchain(
                previous_hash, self.pending_transactions.copy(), nonce, miner_address
            )

            # Check if hash meets difficulty requirement
            if block.block_hash.startswith("0" * self.difficulty):
                # Success! Add block to chain
                self.chain.append(block)

                # Add mining reward transaction
                reward_transaction = (
                    f"MINING_REWARD: {self.mining_reward} MGH to {miner_address}"
                )
                self.pending_transactions = [
                    reward_transaction
                ]  # Start new block with reward

                return {
                    "status": "success",
                    "message": f"Block mined by {miner_address}!",
                    "block_hash": block.block_hash,
                    "nonce": nonce,
                    "difficulty": self.difficulty,
                    "transactions_count": len(block.transaction_list),
                    "mining_reward": self.mining_reward,
                }

            nonce += 1

        return {"status": "error", "message": "Mining failed - too many attempts"}

    def get_mining_info(self) -> dict:
        """Get information needed for mining"""
        return {
            "previous_block_hash": self.chain[-1].block_hash,
            "pending_transactions": self.pending_transactions,
            "difficulty": self.difficulty,
            "min_transactions_required": self.MIN_TRANSACTIONS_PER_BLOCK,
            "max_transactions_per_block": self.MAX_TRANSACTIONS_PER_BLOCK,
        }

    def get_status(self) -> dict:
        """Get blockchain status"""
        return {
            "chain_length": len(self.chain),
            "pending_transactions": len(self.pending_transactions),
            "difficulty": self.difficulty,
            "last_block_hash": self.chain[-1].block_hash if self.chain else None,
            "mining_reward": self.mining_reward,
        }

    def validate_chain(self) -> dict:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if previous block hash matches
            if current_block.previous_block_hash != previous_block.block_hash:
                return {"status": "error", "message": f"Invalid chain at block {i}"}

            # Recalculate hash to ensure integrity
            block_data = (
                " | ".join(current_block.transaction_list)
                + " | "
                + current_block.previous_block_hash
                + " | "
                + str(current_block.nonce)
            )
            calculated_hash = hashlib.sha256(block_data.encode()).hexdigest()

            if calculated_hash != current_block.block_hash:
                return {"status": "error", "message": f"Invalid hash at block {i}"}

        return {"status": "success", "message": "Blockchain is valid"}
