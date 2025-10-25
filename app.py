from flask import Flask, render_template, request
import joblib  # Use joblib (matches how you saved the model)
import numpy as np

app = Flask(__name__)

# Load the trained model (saved with joblib)
model = joblib.load('model/model/heart_model.pkl')

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
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Get probability if available
        if hasattr(model, 'predict_proba'):
            probability = model.predict_proba(features)[0]
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
    app.run(debug=True)
