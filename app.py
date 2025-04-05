from flask import Flask, render_template, jsonify, request, session
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session handling

# Load verbs and words from Excel files
def load_verbs():
    return pd.read_excel("verbs.xlsx", engine="openpyxl")

def load_words():
    return pd.read_excel("non_verbs.xlsx", engine="openpyxl")

verbs = load_verbs()
words = load_words()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-verb", methods=["GET"])
def get_verb():
    selected_forms = request.args.get("forms", "Te Form,Ta Form").split(",")

    # Initialize session if not set
    if "used_verbs" not in session:
        session["used_verbs"] = []

    used_verbs = session["used_verbs"]

    available_verbs = [verb for verb in verbs.to_dict(orient="records") if verb["Dictionary Form"] not in used_verbs]

    # Reset if all verbs are used
    if not available_verbs:
        available_verbs = verbs.to_dict(orient="records")
        session["used_verbs"] = []

    while True:
        verb_row = random.choice(available_verbs)
        chosen_form = random.choice(selected_forms)
        # Add verb to session storage
        session["used_verbs"].append(verb_row["Dictionary Form"])
        session.modified = True  # Ensure session updates

        if (verb_row[chosen_form] != "na"):
            break

    return jsonify({
        "form": chosen_form,
        "verb": verb_row[chosen_form],
        "all_forms": verb_row
    })

@app.route("/get-non-verb", methods=["GET"])
def get_non_verb():
    # Initialize session if not set
    if "used_words" not in session:
        session["used_words"] = []

    used_words = session["used_words"]

    available_words = [word for word in words.to_dict(orient="records") if word["Kanji"] not in used_words]

    # Reset if all words are used
    if not available_words:
        available_words = words.to_dict(orient="records")
        session["used_words"] = []

    word_row = random.choice(available_words)

    # Add word to session storage
    session["used_words"].append(word_row["Kanji"])
    session.modified = True  # Ensure session updates

    return jsonify({
        "kanji": word_row["Kanji"],
        "kana": word_row["Kana"]
    })

@app.route("/reset-session", methods=["POST"])
def reset_session():
    session.pop("used_verbs", None)
    session.pop("used_words", None)
    return jsonify({"message": "Session reset successful"})

if __name__ == "__main__":
    app.run(debug=False)
