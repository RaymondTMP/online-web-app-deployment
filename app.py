from flask import Flask, render_template, jsonify, request, make_response
import pandas as pd
import random
import json

app = Flask(__name__)

# Load verbs from Excel
def load_verbs():
    return pd.read_excel("verbs.xlsx", engine="openpyxl")

verbs = load_verbs()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-verb", methods=["GET"])
def get_verb():
    # Get verb forms from request params (default: ["Te Form", "Ta Form"])
    selected_forms = request.args.getlist("forms[]")
    if not selected_forms:
        selected_forms = ["Te Form", "Ta Form"]  # Default options

    # Get used verbs from cookies
    used_verbs = request.cookies.get("used_verbs")
    used_verbs = json.loads(used_verbs) if used_verbs else []

    available_verbs = verbs.to_dict(orient="records")

    # Filter out already used verbs
    filtered_verbs = [verb for verb in available_verbs if verb["Dictionary Form"] not in used_verbs]

    if not filtered_verbs:  # If all verbs are used, reset history
        used_verbs = []
        filtered_verbs = available_verbs

    # Pick a random verb
    verb_row = random.choice(filtered_verbs)

    # Choose a random selected form
    chosen_form = random.choice(selected_forms)

    # Add selected verb to used list
    used_verbs.append(verb_row["Dictionary Form"])

    # Prepare response
    response_data = {
        "form": chosen_form,
        "verb": verb_row[chosen_form],
        "all_forms": verb_row
    }

    # Create response and set cookie
    response = make_response(jsonify(response_data))
    response.set_cookie("used_verbs", json.dumps(used_verbs), max_age=1800)  # Expires in 1 hour

    return response

@app.route("/reset", methods=["POST"])
def reset_verbs():
    """Manually reset used verbs (clear cookie)."""
    response = make_response(jsonify({"message": "Verb history has been reset."}))
    response.set_cookie("used_verbs", "", expires=0)  # Clear the cookie
    return response

if __name__ == "__main__":
    app.run(debug=False)
