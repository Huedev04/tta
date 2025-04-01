import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        value = str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.data) + str(self.nonce)
        return hashlib.sha256(value.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block, difficulty=4):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
        return True

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount}"

class BlockchainWithTransactions(Blockchain):
    def __init__(self):
        super().__init__()
        self.pending_transactions = []
        self.mining_reward = 50

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address, difficulty=4):
        block = Block(len(self.chain), self.get_latest_block().hash, time.time(), [str(tx) for tx in self.pending_transactions])
        block.mine_block(difficulty)
        self.chain.append(block)
        self.pending_transactions = [Transaction(None, miner_address, self.mining_reward)]

# Khởi tạo Blockchain mới
bank_chain = BlockchainWithTransactions()

# Tạo giao dịch
tx1 = Transaction("Alice", "Bob", 100)
bank_chain.create_transaction(tx1)

# Mine khối mới
bank_chain.mine_pending_transactions("Miner1")

# Kiểm tra tính hợp lệ của chuỗi
print(f"Blockchain valid: {bank_chain.is_chain_valid()}")

# In thông tin các khối trong chuỗi
for block in bank_chain.chain:
    print(f"Block Index: {block.index}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Hash: {block.hash}")
    print(f"Data: {block.data}")
    print("----------------")