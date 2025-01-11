import json
import hashlib

# Function to hash a block
def hash_block(block):
    block_copy = block.copy()
    block_copy.pop('hash', None)  # Remove the hash field before hashing
    encoded_block = json.dumps(block_copy, sort_keys=True).encode()
    return hashlib.sha256(encoded_block).hexdigest()

# Function to verify the integrity of the blockchain
def is_chain_valid(chain):
    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i - 1]
        
        # Verify the previous hash
        if current_block['previous_hash'] != hash_block(previous_block):
            return False
        
        # Verify the current hash
        if current_block['hash'] != hash_block(current_block):
            return False
    
    return True

# Load the blockchain from a JSON file
with open('aroma_blockchain.json', 'r') as f:
    blockchain = json.load(f)

# Run the verification
if is_chain_valid(blockchain):
    print("✅ The blockchain is valid.")
else:
    print("❌ The blockchain is not valid.")
