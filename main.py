from flask import Flask, request, jsonify, send_file, abort
import json
import hashlib
import time
import os

app = Flask(__name__)

# Загрузка блокчейна
with open("aroma_blockchain.json", "r") as f:
    blockchain = json.load(f)

# Эндпоинт для добавления новой покупки
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

    with open("aroma_blockchain.json", "w") as f:
        json.dump(blockchain, f, indent=4)

    return jsonify({"message": "Purchase added successfully!"}), 200

# Эндпоинт для получения всего блокчейна
@app.route('/aroma_blockchain.json', methods=['GET'])
def get_blockchain():
    return send_file("aroma_blockchain.json", mimetype='application/json')

# Эндпоинт для получения блока по индексу
@app.route('/block/<int:index>', methods=['GET'])
def get_block(index):
    if 0 < index <= len(blockchain):
        return jsonify(blockchain[index - 1])
    else:
        abort(404)

# Запуск приложения
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
