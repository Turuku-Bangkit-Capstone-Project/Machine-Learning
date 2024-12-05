from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('model/turuku_sleep_model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # Preprocess the input data as required by your model
    input_data = np.array(data['input']).reshape(1, -1)

    # Make prediction
    prediction = model.predict(input_data)
    output = prediction[0].tolist()

    return jsonify({'prediction': output})

if __name__ == '__main__':
    app.run(debug=True)