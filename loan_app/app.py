"""
Loan Approval Prediction System
Flask Web Application for PythonAnywhere Deployment
Developer: Muhammad Hamza Afzal
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# ─── Label Encoder Setup ────────────────────────────────────────────────────

def setup_encoders():
    gender_le = LabelEncoder()
    education_le = LabelEncoder()
    home_le = LabelEncoder()
    intent_le = LabelEncoder()
    default_le = LabelEncoder()

    gender_le.fit(["male", "female"])
    education_le.fit(["master", "high school", "bachelor", "associate"])
    home_le.fit(["rent", "own", "mortgage", "other"])
    intent_le.fit(["personal", "education", "medical", "venture", "homeimprovement", "debtconsolidation"])
    default_le.fit(["yes", "no"])

    return gender_le, education_le, home_le, intent_le, default_le


gender_le, education_le, home_le, intent_le, default_le = setup_encoders()


# ─── Train / Load Model ─────────────────────────────────────────────────────

MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_model.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "sample_loan_data.csv")


def train_and_save_model():
    """Train model from CSV and save it. Returns (model, accuracy)."""
    df = pd.read_csv(DATA_PATH)

    cat_cols = ["person_gender", "person_education", "person_home_ownership",
                "loan_intent", "previous_loan_defaults_on_file"]
    df[cat_cols] = df[cat_cols].apply(lambda x: x.str.lower())

    df["person_gender"] = gender_le.transform(df["person_gender"])
    df["person_education"] = education_le.transform(df["person_education"])
    df["person_home_ownership"] = home_le.transform(df["person_home_ownership"])
    df["loan_intent"] = intent_le.transform(df["loan_intent"])
    df["previous_loan_defaults_on_file"] = default_le.transform(df["previous_loan_defaults_on_file"])

    X = df.drop("loan_status", axis=1)
    y = df["loan_status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=0
    )

    trained_model = LogisticRegression(max_iter=1000)
    trained_model.fit(X_train, y_train)

    acc = accuracy_score(y_test, trained_model.predict(X_test))

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(trained_model, f)

    return trained_model, round(acc * 100, 1)


def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            trained_model = pickle.load(f)
            return trained_model
    return None


# Load or train model at startup
trained_model = load_model()
model_accuracy = None

if trained_model is None and os.path.exists(DATA_PATH):
    trained_model, model_accuracy = train_and_save_model()


# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", accuracy=model_accuracy)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Validate & encode input
        gender_enc = gender_le.transform([data["person_gender"].lower()])[0]
        education_enc = education_le.transform([data["person_education"].lower()])[0]
        home_enc = home_le.transform([data["person_home_ownership"].lower()])[0]
        intent_enc = intent_le.transform([data["loan_intent"].lower()])[0]
        default_enc = default_le.transform([data["previous_loan_defaults_on_file"].lower()])[0]

        feature_vector = np.array([[
            int(data["person_age"]),
            gender_enc,
            education_enc,
            float(data["person_income"]),
            int(data["person_emp_exp"]),
            home_enc,
            float(data["loan_amnt"]),
            intent_enc,
            float(data["loan_int_rate"]),
            float(data["loan_percent_income"]),
            int(data["cb_person_cred_hist_length"]),
            int(data["credit_score"]),
            default_enc
        ]])

        prediction = trained_model.predict(feature_vector)[0]
        probability = trained_model.predict_proba(feature_vector)[0]

        result = "Approved" if prediction == 1 else "Rejected"
        confidence = round(float(max(probability)) * 100, 1)

        return jsonify({
            "result": result,
            "confidence": confidence,
            "approved_prob": round(float(probability[1]) * 100, 1),
            "rejected_prob": round(float(probability[0]) * 100, 1),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/train", methods=["POST"])
def retrain():
    """Retrain the model (if CSV is present)."""
    global trained_model, model_accuracy
    if not os.path.exists(DATA_PATH):
        return jsonify({"error": "sample_loan_data.csv not found"}), 404
    trained_model, model_accuracy = train_and_save_model()
    return jsonify({"accuracy": model_accuracy})


if __name__ == "__main__":
    app.run(debug=True)
