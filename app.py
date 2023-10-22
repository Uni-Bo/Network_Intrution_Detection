from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__, static_url_path='/static')

# Load the model from the pickle file
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the form data from the request
        protocol_type = int(request.form['protocol_type'])
        service = int(request.form['service'])
        flag = int(request.form['flag'])
        src_bytes = int(request.form['src_bytes'])
        dst_bytes = int(request.form['dst_bytes'])
        same_srv_rate = float(request.form['same_srv_rate'])
        diff_srv_rate = float(request.form['diff_srv_rate'])
        dst_host_srv_count = int(request.form['dst_host_srv_count'])
        dst_host_same_srv_rate = float(request.form['dst_host_same_srv_rate'])
        dst_host_same_srv_port_rate = float(request.form['dst_host_same_srv_port_rate'])

        # Process the data and make the prediction using the loaded model
        data = {
            "protocol_type": protocol_type,
            "service": service,
            "flag": flag,
            "src_bytes": src_bytes,
            "dst_bytes": dst_bytes,
            "same_srv_rate": same_srv_rate,
            "diff_srv_rate": diff_srv_rate,
            "dst_host_srv_count": dst_host_srv_count,
            "dst_host_same_srv_rate": dst_host_same_srv_rate,
            "dst_host_same_srv_port_rate": dst_host_same_srv_port_rate
        }

        # Convert the dictionary to a DataFrame and reshape it for prediction
        df = pd.DataFrame([data])
        first_element = df.iloc[0]
        first_element_array = np.array(first_element)
        first_element_reshaped = first_element_array.reshape(1, -1)

        # Make the prediction
        prediction = model.predict(first_element_reshaped)
        prediction_value = "Safe" if prediction == 0 else "Not Safe"

        # Return the prediction as a JSON response
        return jsonify({'prediction': prediction_value})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
