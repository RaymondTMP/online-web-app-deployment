from flask import Flask, jsonify
import pandas as pd
import random

app = Flask(__name__)

# Load verbs from an Excel file
def load_verbs():
    return pd.read_excel("verbs.xlsx", engine="openpyxl")

verbs = load_verbs()

@app.route("/get-verb", methods=["GET"])
def get_verb():
    verb_row = verbs.sample(n=1).to_dict(orient="records")[0]  # Pick a random verb
    chosen_form = random.choice(["Te Form", "Ta Form", "Nai Form", "Masu Form"])

    return jsonify({
        "form": chosen_form,
        "verb": verb_row[chosen_form],
        "all_forms": verb_row
    })

if __name__ == "__main__":
    app.run(debug=False)
