from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("usdt_rwf_model.pkl")

@app.route("/")
def home():
    return "USDT/RWF Predictor API Running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    price = float(data.get("price"))
    ret = float(data.get("ret"))
    pred = model.predict([[price, ret]])[0]
    return jsonify({
        "prediction": "UP" if pred == 1 else "DOWN",
        "probability_up": float(model.predict_proba([[price, ret]])[0,1])
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
