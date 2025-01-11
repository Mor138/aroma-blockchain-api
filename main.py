from flask import Flask, request, jsonify, send_file, abort
import json
import hashlib
import time
import os
import requests

app = Flask(__name__)

# Загрузка блокчейна
blockchain_file = "aroma_blockchain.json"
with open(blockchain_file, "r") as f:
    blockchain = json.load(f)

# Функция для загрузки блокчейна на GitHub
def upload_to_github():
    url = "https://api.github.com/repos/Mor138/aroma-blockchain-api/contents/aroma_blockchain.json"
    token = os.environ.get("GITHUB_TOKEN")

    with open(blockchain_file, "r") as file:
        content = file.read()

    # Получаем текущий SHA для файла
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        sha = response.json()["sha"]
    else:
        print("❌ Не удалось получить SHA для файла.")
        return

    # Подготовка данных для загрузки
    data = {
        "message": "Обновление блокчейна",
        "content": content.encode("utf-8").decode("latin1").encode("base64").decode(),
        "sha": sha
    }

    # Отправка запроса на обновление файла
    response = requests.put(url, json=data, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        print("✅ Блокчейн успешно загружен на GitHub.")
    else:
        print("❌ Ошибка при загрузке на GitHub:", response.json())

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

    with open(blockchain_file, "w") as f:
        json.dump(blockchain, f, indent=4)

    # Загрузка на GitHub
    upload_to_github()

    return jsonify({"message": "Purchase added successfully!"}), 200

# Эндпоинт для получения всего блокчейна
@app.route('/aroma_blockchain.json', methods=['GET'])
def get_blockchain():
    return send_file(blockchain_file, mimetype='application/json')

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
