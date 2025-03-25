from flask import Flask, render_template, jsonify, request
import pandas as pd
import random

app = Flask(__name__)

# Load verbs from an Excel file
def load_verbs():
    return pd.read_excel("verbs.xlsx", engine="openpyxl")

verbs = load_verbs()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-verb", methods=["GET"])
def get_verb():
    # Get selected forms from the frontend (default: ["Te Form", "Ta Form"])
    selected_forms = request.args.get("forms", "Te Form,Ta Form").split(",")

    # Get the list of used verbs from the frontend
    used_verbs = request.args.get("usedVerbs", "").split(",") if request.args.get("usedVerbs") else []

    # Filter out used verbs
    available_verbs = [verb for verb in verbs.to_dict(orient="records") if verb["Dictionary Form"] not in used_verbs]

    # If all verbs have been used, reset
    if not available_verbs:
        available_verbs = verbs.to_dict(orient="records")
        used_verbs = []  # Reset used verbs

    # Pick a new random verb
    verb_row = random.choice(available_verbs)

    # Pick a random form from the selected forms
    chosen_form = random.choice(selected_forms)

    return jsonify({
        "form": chosen_form,
        "verb": verb_row[chosen_form],
        "all_forms": verb_row,
        "usedVerbs": used_verbs + [verb_row["Dictionary Form"]]  # Send updated list back
    })

if __name__ == "__main__":
    app.run(debug=False)
