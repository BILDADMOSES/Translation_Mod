from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import pickle
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app)

rooms = {}

# Load the language detection model
language_model_ckpt = "papluca/xlm-roberta-base-language-detection"
language_tokenizer = AutoTokenizer.from_pretrained(language_model_ckpt)
language_model = AutoModelForSequenceClassification.from_pretrained(language_model_ckpt)

# Load the English-to-Swahili translation model
eng_to_swa_model_info = pickle.load(open('Eng_to_Swa_Translator_info.pkl', 'rb'))
eng_to_swa_tokenizer = AutoTokenizer.from_pretrained(eng_to_swa_model_info["model_name"])
eng_to_swa_model = AutoModelForSeq2SeqLM.from_pretrained(eng_to_swa_model_info["model_name"])

# Load the Swahili-to-English translation model
swa_to_eng_model_info = pickle.load(open('Swa_to_Eng_Translator_info.pkl', 'rb'))
swa_to_eng_tokenizer = AutoTokenizer.from_pretrained(swa_to_eng_model_info["model_name"])
swa_to_eng_model = AutoModelForSeq2SeqLM.from_pretrained(swa_to_eng_model_info["model_name"])

def detect_language(text):
    inputs = language_tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        logits = language_model(**inputs).logits
    preds = torch.softmax(logits, dim=-1)
    id2lang = language_model.config.id2label
    vals, idxs = torch.max(preds, dim=1)
    return id2lang[idxs[0].item()]

def translate_text(tokenizer, model, text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

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
    
    message_text = data["data"]

    # Detect language
    language = detect_language(message_text)

    # Translate based on detected language
    if language == "en":
        translated_message = translate_text(eng_to_swa_tokenizer, eng_to_swa_model, message_text)
    elif language == "sw":
        translated_message = translate_text(swa_to_eng_tokenizer, swa_to_eng_model, message_text)
    else:
        translated_message = "Language not supported"

    content_sender = {
        "name": session.get("name"),
        "message": message_text
    }

    content_receiver = {
        "name": session.get("name"),
        "message": translated_message
    }
    
    # Send the original message to the sender and the translated message to others in the room
    send(content_sender, to=request.sid)
    send(content_receiver, to=room, skip_sid=request.sid)
    
    rooms[room]["messages"].append(content_receiver)
    print(f"{session.get('name')} said: {message_text}")

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
    send({"name": name, "message": "has entered the room "}, to=room)
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
