# Healthcare Fraud Detection System - Deployment

## 🚀 Quick Start

### Option 1: Run Locally
```bash
# Install dependencies
cd experiments/day6_deployment/api
pip install -r requirements.txt

# Run API server
python app.py

# Open frontend in browser
# Open experiments/day6_deployment/frontend/index.html
```

### Option 2: Run with Docker
```bash
cd experiments/day6_deployment/docker
docker-compose up
```

Access:
- API: http://localhost:5000
- Frontend: http://localhost:8080

## 📡 API Endpoints

### GET /
API information and available endpoints

### GET /health
Health check

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-03-07T10:30:00",
  "models_loaded": {
    "random_forest": true,
    "lstm": true,
    "isolation_forest": true
  }
}
```

### POST /predict
Predict fraud for a single claim

**Request:**
```json
{
  "ClaimAmount": 5000.0,
  "InscClaimAmtReimbursed": 4500.0,
  "DeductibleAmtPaid": 500.0,
  "ClaimDuration": 5,
  "ClaimMonth": 3
}
```

**Response:**
```json
{
  "status": "success",
  "predictions": {
    "ensemble": {
      "fraud_probability": 0.85,
      "prediction": "FRAUD",
      "confidence": 0.85,
      "risk_level": "HIGH"
    }
  }
}
```

## 🏗️ Architecture
```
┌─────────────┐
│   Frontend  │ (HTML/JS)
│  (Port 8080)│
└──────┬──────┘
       │ HTTP
┌──────▼──────┐
│  Flask API  │ (Python)
│  (Port 5000)│
└──────┬──────┘
       │
┌──────▼──────────────────┐
│   Trained Models        │
│  ├─ Random Forest       │
│  ├─ LSTM                │
│  ├─ Isolation Forest    │
│  └─ Ensemble Config     │
└─────────────────────────┘
```

## 📊 Models

- **Random Forest**: Baseline model (F1=0.86)
- **LSTM**: Temporal patterns (F1=0.85)
- **Isolation Forest**: Financial anomalies (F1=0.82)
- **Ensemble**: Combined (F1=0.90+)

## 🔒 Security

- CORS enabled for web access
- Input validation
- Error handling
- Rate limiting (recommended for production)

## 📈 Performance

- Response time: < 100ms
- Throughput: 100+ requests/sec
- Accuracy: 96.7%

## 🛠️ Production Deployment

For production:

1. Use Gunicorn instead of Flask dev server
2. Set up HTTPS
3. Add authentication
4. Implement rate limiting
5. Set up monitoring (Prometheus/Grafana)
6. Use proper logging

## 📝 License

MIT License - P. Chandrasekaran

## 👤 Author

**P. Chandrasekaran**
- M.Tech AI/ML, BITS Pilani
- Research: Multi-Modal Fraud Detection
- GitHub: github.com/chandrasekaranp/healthcare-fraud-detection
