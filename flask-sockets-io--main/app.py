from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import pickle
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app)

rooms = {}

# Load the model information
with open('Swa_to_Eng_Translator_info.pkl', 'rb') as info_file:
    model_info = pickle.load(info_file)

# Load the tokenizer and model
translator_tokenizer = AutoTokenizer.from_pretrained(model_info["model_name"])
translator_model = AutoModelForSeq2SeqLM.from_pretrained(model_info["model_name"])

def translate_text(french_text: str) -> str:
    # Tokenize the French text
    inputs = translator_tokenizer(french_text, return_tensors="pt", padding=True, truncation=True)
    # Generate the English translation
    outputs = translator_model.generate(**inputs)
    # Decode the English translation
    english_text = translator_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return english_text

def generate_unique_code(length):
    while True:
        code = "".join(random.choice(ascii_uppercase) for _ in range(length))
        if code not in rooms:
            break
    return code

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/home", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    # Translate the message
    translated_message = translate_text(data["data"])

    # Original message for sender
    original_content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    # Translated message for recipient
    translated_content = {
        "name": session.get("name"),
        "message": translated_message
    }

    # Send only the original message to the sender
    send(original_content, to=request.sid)

    # Send only the translated message to the room except the sender
    send(translated_content, to=room, skip_sid=request.sid)

    # Update the room's message history with both original and translated messages
    rooms[room]["messages"].append(original_content)
    rooms[room]["messages"].append(translated_content)

    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

if __name__ == "__main__":
    socketio.run(app, debug=True)
