from flask import Flask, request, jsonify
import json
import hashlib
import time

app = Flask(__name__)

# Load the blockchain from the JSON file
with open("aroma_blockchain.json", "r") as f:
    blockchain = json.load(f)

# API endpoint to add a new purchase
@app.route('/add_purchase', methods=['POST'])
def add_purchase():
    data = request.json
    previous_block = blockchain[-1]
    
    new_block = {
        "index": len(blockchain) + 1,
        "timestamp": time.time(),
        "aromatic_code": data.get("aromatic_code"),
        "hashed_code": hashlib.sha256(data.get("aromatic_code").encode()).hexdigest(),
        "signature": data.get("signature"),
        "public_key": data.get("public_key"),
        "previous_hash": previous_block["hash"]
    }
    new_block["hash"] = hashlib.sha256(json.dumps(new_block, sort_keys=True).encode()).hexdigest()
    
    blockchain.append(new_block)
    
    # Save updated blockchain to the file
    with open("aroma_blockchain.json", "w") as f:
        json.dump(blockchain, f, indent=4)

    return jsonify({"message": "Purchase added successfully!"}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
