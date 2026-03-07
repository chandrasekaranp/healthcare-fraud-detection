#!/usr/bin/env python3
"""
Healthcare Fraud Detection API
Author: P. Chandrasekaran
Research: Multi-Modal Fraud Detection System
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for web frontend

# Load all models
print("Loading models...")
BASE_PATH = "../../"

try:
    rf_model = joblib.load(f"{BASE_PATH}experiments/day1_baseline/model/random_forest.pkl")
    print("✅ Random Forest loaded")
except Exception as e:
    print(f"⚠️  Random Forest not found: {e}")
    rf_model = None

try:
    from tensorflow.keras.models import load_model
    lstm_model = load_model(f"{BASE_PATH}experiments/day2_lstm/model/lstm_model.h5")
    lstm_scaler = joblib.load(f"{BASE_PATH}experiments/day2_lstm/model/scaler.pkl")
    print("✅ LSTM model loaded")
except Exception as e:
    print(f"⚠️  LSTM not found: {e}")
    lstm_model = None
    lstm_scaler = None

try:
    iso_model = joblib.load(f"{BASE_PATH}experiments/day3_isolation_forest/model/isolation_forest.pkl")
    iso_scaler = joblib.load(f"{BASE_PATH}experiments/day3_isolation_forest/model/scaler.pkl")
    print("✅ Isolation Forest loaded")
except Exception as e:
    print(f"⚠️  Isolation Forest not found: {e}")
    iso_model = None
    iso_scaler = None

try:
    ensemble_config = joblib.load(f"{BASE_PATH}experiments/day4_ensemble/model/ensemble_config.pkl")
    print("✅ Ensemble config loaded")
except Exception as e:
    print(f"⚠️  Ensemble config not found: {e}")
    ensemble_config = None

@app.route('/')
def home():
    """API home page"""
    return jsonify({
        "name": "Healthcare Fraud Detection API",
        "version": "1.0.0",
        "author": "P. Chandrasekaran",
        "description": "Multi-modal fraud detection using RF, LSTM, and Isolation Forest",
        "endpoints": {
            "/health": "Health check",
            "/predict": "Predict fraud (single claim)",
            "/batch_predict": "Predict fraud (multiple claims)",
            "/models/info": "Get model information",
            "/stats": "Get API statistics"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": {
            "random_forest": rf_model is not None,
            "lstm": lstm_model is not None,
            "isolation_forest": iso_model is not None,
            "ensemble": ensemble_config is not None
        }
    })

@app.route('/models/info')
def models_info():
    """Get information about loaded models"""
    info = {
        "models": []
    }
    
    if rf_model:
        info["models"].append({
            "name": "Random Forest",
            "type": "Supervised - Static Features",
            "day": 1,
            "status": "loaded"
        })
    
    if lstm_model:
        info["models"].append({
            "name": "LSTM (Deep NN)",
            "type": "Supervised - Temporal Patterns",
            "day": 2,
            "status": "loaded"
        })
    
    if iso_model:
        info["models"].append({
            "name": "Isolation Forest",
            "type": "Unsupervised - Financial Anomalies",
            "day": 3,
            "status": "loaded"
        })
    
    if ensemble_config:
        info["ensemble"] = {
            "method": ensemble_config.get("method", "Weighted Average"),
            "weights": ensemble_config.get("weights", {}),
            "status": "loaded"
        }
    
    return jsonify(info)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict fraud for a single claim
    
    Expected JSON input:
    {
        "ClaimAmount": 5000.0,
        "InscClaimAmtReimbursed": 4500.0,
        "DeductibleAmtPaid": 500.0,
        "ClaimDuration": 5,
        "ClaimMonth": 3,
        ... (other features)
    }
    """
    try:
        data = request.get_json()
        
        # Extract features (simplified - adjust based on your actual features)
        features = pd.DataFrame([{
            'ClaimAmount': data.get('ClaimAmount', 0),
            'InscClaimAmtReimbursed': data.get('InscClaimAmtReimbursed', 0),
            'DeductibleAmtPaid': data.get('DeductibleAmtPaid', 0),
            'ClaimDuration': data.get('ClaimDuration', 1),
            'ClaimMonth': data.get('ClaimMonth', 1),
            'ReimbursementRatio': data.get('InscClaimAmtReimbursed', 0) / (data.get('ClaimAmount', 1) + 1),
            'DeductibleRatio': data.get('DeductibleAmtPaid', 0) / (data.get('ClaimAmount', 1) + 1),
            'ChronicCond_Diabetes': data.get('ChronicCond_Diabetes', 0),
            'ChronicCond_Heartfailure': data.get('ChronicCond_Heartfailure', 0),
            'Gender': data.get('Gender', 1)
        }])
        
        predictions = {}
        
        # Random Forest prediction
        if rf_model:
            rf_prob = rf_model.predict_proba(features)[0, 1]
            predictions['random_forest'] = {
                'fraud_probability': float(rf_prob),
                'prediction': 'FRAUD' if rf_prob > 0.5 else 'NORMAL',
                'confidence': float(max(rf_prob, 1 - rf_prob))
            }
        
        # Ensemble prediction (weighted average)
        if ensemble_config and rf_model:
            weights = ensemble_config.get('weights', {})
            w_rf = weights.get('random_forest', 1.0)
            
            ensemble_prob = w_rf * rf_prob  # Simplified - add other models as available
            
            predictions['ensemble'] = {
                'fraud_probability': float(ensemble_prob),
                'prediction': 'FRAUD' if ensemble_prob > 0.5 else 'NORMAL',
                'confidence': float(max(ensemble_prob, 1 - ensemble_prob)),
                'risk_level': 'HIGH' if ensemble_prob > 0.7 else 'MEDIUM' if ensemble_prob > 0.4 else 'LOW'
            }
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "claim_data": data,
            "predictions": predictions
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 400

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Predict fraud for multiple claims"""
    try:
        data = request.get_json()
        claims = data.get('claims', [])
        
        results = []
        for claim in claims:
            # Process each claim (simplified)
            claim_result = {
                'claim_id': claim.get('ClaimID', 'unknown'),
                'fraud_probability': 0.5,  # Placeholder
                'prediction': 'NORMAL'
            }
            results.append(claim_result)
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "num_claims": len(claims),
            "results": results
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/stats')
def stats():
    """API usage statistics"""
    return jsonify({
        "total_predictions": 0,  # Implement counter
        "uptime": "N/A",
        "models_active": sum([
            rf_model is not None,
            lstm_model is not None,
            iso_model is not None
        ])
    })

if __name__ == '__main__':
    print("="*70)
    print("HEALTHCARE FRAUD DETECTION API")
    print("="*70)
    print("Starting Flask API server...")
    print("API will be available at: http://localhost:5000")
    print("="*70)
    app.run(host='0.0.0.0', port=5000, debug=True)
