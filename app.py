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

if __name__ == "__main__":
    app.run(debug=False)
