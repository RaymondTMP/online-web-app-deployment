from flask import Flask, render_template, jsonify, request
import pandas as pd
import random

app = Flask(__name__)

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
    used_verbs = request.args.get("usedVerbs", "").split(",") if request.args.get("usedVerbs") else []

    available_verbs = [verb for verb in verbs.to_dict(orient="records") if verb["Dictionary Form"] not in used_verbs]

    if not available_verbs:
        available_verbs = verbs.to_dict(orient="records")
        used_verbs = []

    verb_row = random.choice(available_verbs)
    chosen_form = random.choice(selected_forms)

    return jsonify({
        "form": chosen_form,
        "verb": verb_row[chosen_form],
        "all_forms": verb_row,
        "usedVerbs": used_verbs + [verb_row["Dictionary Form"]]
    })

@app.route("/get-non-verb", methods=["GET"])
def get_non_verb():
    used_words = request.args.get("usedWords", "").split(",") if request.args.get("usedWords") else []

    available_words = [word for word in words.to_dict(orient="records") if word["Kanji"] not in used_words]

    if not available_words:
        available_words = words.to_dict(orient="records")
        used_words = []

    word_row = random.choice(available_words)

    return jsonify({
        "kanji": word_row["Kanji"],
        "kana": word_row["Kana"],
        "usedWords": used_words + [word_row["Kanji"]]
    })

if __name__ == "__main__":
    app.run(debug=False)
