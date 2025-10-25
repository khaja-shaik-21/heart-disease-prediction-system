from flask import Flask, render_template, request
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load the trained model and scaler
model_path = os.path.join('model', 'model', 'heart_model.pkl')
scaler_path = os.path.join('model', 'model', 'scaler.pkl')

if not os.path.exists(model_path):
    # Try alternative path
    model_path = os.path.join('model', 'heart_model.pkl')
    scaler_path = os.path.join('model', 'scaler.pkl')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        age = int(request.form['age'])
        sex = int(request.form['sex'])
        cp = int(request.form['cp'])
        trestbps = int(request.form['trestbps'])
        chol = int(request.form['chol'])
        fbs = int(request.form['fbs'])
        restecg = int(request.form['restecg'])
        thalach = int(request.form['thalach'])
        exang = int(request.form['exang'])
        oldpeak = float(request.form['oldpeak'])
        slope = int(request.form['slope'])
        ca = int(request.form['ca'])
        thal = int(request.form['thal'])
        
        # Create feature array
        features = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, 
                              thalach, exang, oldpeak, slope, ca, thal]])
        
        # Scale the features (IMPORTANT: Must scale before prediction)
        features_scaled = scaler.transform(features)
        
        # Make prediction on scaled data
        prediction = model.predict(features_scaled)[0]
        
        # Get probability if available
        if hasattr(model, 'predict_proba'):
            probability = model.predict_proba(features_scaled)[0]
            confidence = round(max(probability) * 100, 2)
        else:
            confidence = None
        
        return render_template('result.html', 
                             prediction=prediction, 
                             confidence=confidence)
    
    except Exception as e:
        return render_template('result.html', 
                             prediction=None, 
                             error=str(e))

if __name__ == '__main__':
    # Use PORT environment variable for deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)