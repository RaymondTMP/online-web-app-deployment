from flask import Flask, render_template, jsonify
import pandas as pd
import random
import json  # ✅ Import Python's built-in JSON module

app = Flask(__name__)

# Load verbs from an Excel file
def load_verbs():
    return pd.read_excel("verbs.xlsx", engine="openpyxl")

verbs = load_verbs()

@app.route("/")
def home():
    """Serve the HTML page."""
    return render_template("index.html")


@app.route("/get-verb", methods=["GET"])
def get_verb():
    verb_row = verbs.sample(n=1).to_dict(orient="records")[0] 
    chosen_form = random.choice(["Te Form", "Ta Form"])

   
    response_data = json.dumps({
        "form": chosen_form,
        "verb": verb_row[chosen_form],
        "all_forms": verb_row
    }, ensure_ascii=False)

    return app.response_class(response=response_data, mimetype="application/json")

if __name__ == "__main__":
    app.run(debug=False)
