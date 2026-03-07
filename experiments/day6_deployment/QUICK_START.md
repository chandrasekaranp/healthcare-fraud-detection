# 🚀 QUICK START GUIDE

## 1. Start the API (Terminal 1)
```bash
cd experiments/day6_deployment/api
pip install -r requirements.txt
python app.py
```

You should see:
```
Healthcare Fraud Detection API starting on http://localhost:5000
```

## 2. Open Frontend (Terminal 2)

Simply open this file in your web browser:
```
experiments/day6_deployment/frontend/index.html
```

OR use a simple HTTP server:
```bash
cd experiments/day6_deployment/frontend
python -m http.server 8080
```

Then open: http://localhost:8080

## 3. Test the System

1. Open the frontend in your browser
2. Enter claim details
3. Click "Analyze Fraud Risk"
4. View results!

## 4. Test API Directly (Optional)
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"ClaimAmount": 10000, "InscClaimAmtReimbursed": 9000, "DeductibleAmtPaid": 1000, "ClaimDuration": 7, "ClaimMonth": 6}'
```

## Done! 🎉

Your fraud detection system is now live and ready to use!
