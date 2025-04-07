from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("models/svc.pkl")

# Load data from CSV files
medications_df = pd.read_csv("medications.csv")
symptoms_df = pd.read_csv("symptoms.csv")
diet_df = pd.read_csv("diet.csv")
precaution_df = pd.read_csv("precaution.csv")
description_df = pd.read_csv("description.csv")

# Extract symptom columns (assumes 'Disease' is the first column)
symptom_columns = list(symptoms_df.columns[1:])

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    input_symptoms = data.get("symptoms")

    if not input_symptoms:
        return jsonify({"error": "No symptoms provided"}), 400

    # Create binary vector for symptoms
    input_vector = [1 if col in input_symptoms else 0 for col in symptom_columns]
    prediction = model.predict([input_vector])[0]

    # Fetch associated data for predicted disease
    try:
        description = description_df.loc[description_df['Disease'] == prediction, 'Description'].values[0]
        precautions = precaution_df.loc[precaution_df['Disease'] == prediction].values[0][1:]
        medications = medications_df.loc[medications_df['Disease'] == prediction].values[0][1:]
        diet = diet_df.loc[diet_df['Disease'] == prediction].values[0][1:]
    except IndexError:
        return jsonify({"error": f"No information found for disease: {prediction}"}), 500

    return jsonify({
        "predicted_disease": prediction,
        "description": description,
        "precautions": [p for p in precautions if pd.notna(p)],
        "medications": [m for m in medications if pd.notna(m)],
        "diet": [d for d in diet if pd.notna(d)],
        "workout": ["Exercise regularly", "Stay hydrated", "Maintain hygiene"]
    })

if __name__ == "__main__":
    app.run(debug=True)
