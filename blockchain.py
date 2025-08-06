import hashlib

class MGHBlockchain:
    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = " | ".join(transaction_list) + " | " + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

    

t1 = "Anna send 1 MGH to Bob"
t2 = "Bob send 2.1 MGH to Charlie"
t3 = "Charlie send 4 MGH to David"
t4 = "Bob send 0.5 MGH to Anna"
t5 = "David send 1.5 MGH to Bob"
t6 = "Charlie send 3 MGH to Bob"
t7 = "Bob send 0.5 MGH to Anna"
t8 = "Anna send 1.5 MGH to Bob"
t9 = "Charlie send 0.5 MGH to Bob"
t10 = "Bob send 0.5 MGH to Anna"


initial_block = MGHBlockchain("Genesis Block", [t1, t2])

print(initial_block.block_data)
print(initial_block.block_hash)







