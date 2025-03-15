import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify

# 🔥 Initialisation de Firebase
cred = credentials.Certificate("chapp-bb571-firebase-adminsdk-fbsvc-1d1ceacd36.json")  # 🔑 Fichier JSON des clés Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chapp-bb571-default-rtdb.firebaseio.com/'  # Remplace par l'URL de ta base Firebase
})

app = Flask(__name__)

# 🔥 Route pour envoyer un message
@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    user = data.get("user")
    message = data.get("message")

    if not user or not message:
        return jsonify({"error": "User et message requis"}), 400

    ref = db.reference("/messages").push({
        "user": user,
        "message": message
    })

    return jsonify({"success": True, "id": ref.key})

# 🔥 Route pour récupérer les messages
@app.route('/messages', methods=['GET'])
def get_messages():
    ref = db.reference("/messages")
    messages = ref.get()

    return jsonify(messages if messages else {})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
