from flask import Flask, render_template, request
import pickle
import pandas as pd
from utils import preprocess
import os

app = Flask(__name__)

# Load model & vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Load quotes
quotes = pd.read_csv("quotes.csv")

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    emotion = ""

    if request.method == "POST":
        text = request.form["text"]

        #Preprocess
        clean = preprocess(text)
        vec = vectorizer.transform([clean])

        # ML prediction
        emotion = model.predict(vec)[0]

        text_lower = text.lower()

        if any(word in text_lower for word in ["sad", "bad", "depressed", "upset", "tired","low "]):
            emotion = "sad"
        elif any(word in text_lower for word in ["happy", "great", "awesome", "good", "excited"]):
            emotion = "happy"
        elif any(word in text_lower for word in ["angry", "hate", "mad", "furious"]):
            emotion = "angry"
        elif any(word in text_lower for word in ["fear", "scared", "afraid", "nervous"]):
            emotion = "fear"
        elif any(word in text_lower for word in ["surprise", "shocked", "wow"]):
            emotion = "surprise"

        # Get quote
        filtered = quotes[quotes["emotion"] == emotion]

        if len(filtered) > 0:
            result = "\n".join(filtered.sample(min(3, len(filtered)))["quote"].values)
        else:
            result = "Stay strong"

    return render_template("index.html", result=result, emotion=emotion)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)