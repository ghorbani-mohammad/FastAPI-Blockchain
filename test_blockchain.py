import unittest
from blockchain import MGHBlockchain


class TestMGHBlockchain(unittest.TestCase):

    def test_genesis_block(self):
        """Test the genesis block with Anna and Bob transactions"""
        t1 = "Anna send 1 MGH to Bob"
        t2 = "Bob send 2.1 MGH to Charlie"

        genesis_block = MGHBlockchain("Genesis Block", [t1, t2])

        # Test expected block data
        expected_block_data = (
            "Anna send 1 MGH to Bob | Bob send 2.1 MGH to Charlie | Genesis Block"
        )
        self.assertEqual(genesis_block.block_data, expected_block_data)

        # Test expected hash
        expected_hash = (
            "5edce08c5f27ec457650b62fa85c121de34579a8a9b9d0ecbeb13578f1f4f666"
        )
        self.assertEqual(genesis_block.block_hash, expected_hash)

    def test_second_block(self):
        """Test the second block with Charlie, Bob, and David transactions"""
        t3 = "Charlie send 4 MGH to David"
        t4 = "Bob send 0.5 MGH to Anna"
        t5 = "David send 1.5 MGH to Bob"

        # Use the genesis block hash as previous block hash
        genesis_hash = (
            "5edce08c5f27ec457650b62fa85c121de34579a8a9b9d0ecbeb13578f1f4f666"
        )
        second_block = MGHBlockchain(genesis_hash, [t3, t4, t5])

        # Test expected block data
        expected_block_data = "Charlie send 4 MGH to David | Bob send 0.5 MGH to Anna | David send 1.5 MGH to Bob | 5edce08c5f27ec457650b62fa85c121de34579a8a9b9d0ecbeb13578f1f4f666"
        self.assertEqual(second_block.block_data, expected_block_data)

        # Test expected hash
        expected_hash = (
            "6c6594358b10e4b9032742a14f85af0bade67ce9854f631a7922d90031f9cff6"
        )
        self.assertEqual(second_block.block_hash, expected_hash)

    def test_block_chain_integrity(self):
        """Test that blocks can be chained together properly"""
        t1 = "Anna send 1 MGH to Bob"
        t2 = "Bob send 2.1 MGH to Charlie"

        genesis_block = MGHBlockchain("Genesis Block", [t1, t2])

        t3 = "Charlie send 4 MGH to David"
        t4 = "Bob send 0.5 MGH to Anna"
        t5 = "David send 1.5 MGH to Bob"

        second_block = MGHBlockchain(genesis_block.block_hash, [t3, t4, t5])

        # Verify the second block references the first block's hash
        self.assertEqual(second_block.previous_block_hash, genesis_block.block_hash)

        # Verify the block data includes the previous block hash
        self.assertIn(genesis_block.block_hash, second_block.block_data)


if __name__ == "__main__":
    unittest.main()
