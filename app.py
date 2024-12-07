import os
import mysql.connector
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from jwt.exceptions import InvalidTokenError, DecodeError
import pandas as pd
from tensorflow import keras
import joblib
import numpy as np
from dotenv import load_dotenv

load_dotenv()

env_jwt_key = os.getenv("JWT_SECRET_KEY")
env_chronotype_model = os.getenv("CHRONOTYPE_MODEL")
env_chronotype_scaler = os.getenv("CHRONOTYPE_SCALER")
env_chronotype_label_encoder = os.getenv("CHRONOTYPE_LABEL_ENCODER")
env_sleep_model = os.getenv("SLEEP_MODEL")
env_sleep_scaler = os.getenv("SLEEP_SCALER")


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = env_jwt_key
jwt = JWTManager(app)

chronotype_model = keras.models.load_model(env_chronotype_model)
chronotype_scaler = joblib.load(env_chronotype_scaler)
chronotype_label_encoder = joblib.load(env_chronotype_label_encoder)
sleep_model = keras.models.load_model(env_sleep_model,custom_objects={'mse': 'mse'})
sleep_scaler = joblib.load(env_sleep_scaler)


@app.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return jsonify({'success': False, 'message': 'Missing Authorization Header'}), 401


@app.errorhandler(InvalidHeaderError)
def handle_invalid_header_error(e):
    return jsonify({'success': False, 'message': str(e)}), 422


@app.errorhandler(InvalidTokenError)
def handle_invalid_token_error(e):
    return jsonify({'success': False, 'message': str(e)}), 422


@app.errorhandler(DecodeError)
def handle_decode_error(e):
    return jsonify({'success': False, 'message': 'Invalid token'}), 422

mydb = mysql.connector.connect(
    host="http://34.50.69.77/",
    user="myuser",
    password="saljusemihujan"
)

mycursor = mydb.cursor() 

mycursor.execute("SELECT * FROM history")

myresult = mycursor.fetchall()

def validate_chronotype(data):
    if not isinstance(data, dict):
        return False, "Input harus berupa objek JSON."

    if 'bedtime_hour' not in data or 'wakeup_hour' not in data:
        return False, "Bedtime_Hour dan Wakeup_Hour wajib ada."
    
    for row in myresult:
        bedtime_hour = data.get(row[0])
        wakeup_hour = data.get(row[1])

    if not isinstance(bedtime_hour, int) or not 0 <= bedtime_hour <= 23:
        return False, "Bedtime_Hour harus berupa integer antara 0 dan 23."

    if not isinstance(wakeup_hour, int) or not 0 <= wakeup_hour <= 23:
        return False, "Wakeup_Hour harus berupa integer antara 0 dan 23."

    return True, ""


def get_sleep_recommendation(predicted_duration):
    """Menghasilkan rekomendasi berdasarkan prediksi."""
    if predicted_duration < 7:
        recommendation = predicted_duration + 1  # Contoh: Tambah 1 jam jika kurang dari 7
    elif predicted_duration > 9:
        recommendation = predicted_duration -1  # Contoh: Kurangi 1 jam jika lebih dari 9
    else:
        recommendation = predicted_duration
    return recommendation


def format_duration(hours):
    """Memformat durasi tidur ke format HH:MM."""
    minutes = int(round((hours * 60) % 60))
    hours = int(hours)
    return f"{hours:02}:{minutes:02}"


# Sample input
# Header (Authorization): Bearer <your_token>
# 
# {
#   "bedtime_hour": 23,
#   "wakeup_hour": 5
# }
@app.route('/chronotype', methods=['POST'])
# @jwt_required()
def chronotype_classification():
    try:
        data = request.get_json()

        is_valid, error_message = validate_chronotype(data)
        if not is_valid:
            return jsonify({'message': error_message}), 400
        
        bedtime_hour = data['bedtime_hour']
        wakeup_hour = data['wakeup_hour']

        input_data = [[bedtime_hour, wakeup_hour]]
        input_df = pd.DataFrame(input_data, columns=['Bedtime_Hour', 'Wakeup_Hour'])
        scaled_input = chronotype_scaler.transform(input_df)
        prediction = chronotype_model.predict(scaled_input)
        predicted_class = chronotype_label_encoder.inverse_transform([prediction.argmax()])[0]

        return jsonify({
            'success': True,
            'message': 'success',
            'chronotype': predicted_class
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# Sample input
# Header (Authorization): Bearer <your_token>
# 
# {
#   "daily_steps": 0.6175167881125876,
#   "physical_activity_level": 70,
#   "age": 25,
#   "gender": 1,
#   "chronotype": 2
# }
@app.route('/sleep', methods=['POST'])
# @jwt_required()
def sleep_recommendation():
    try:
        data = request.get_json()
        daily_steps = float(data.get('daily_steps'))
        physical_activity = int(data.get('physical_activity_level'))
        age = int(data.get('age'))
        gender = int(data.get('gender'))
        chronotype = int(data.get('chronotype'))

        input_data = np.array([[daily_steps, physical_activity, age, gender, chronotype]])

        predicted_duration_scaled = sleep_model.predict(input_data)[0][0]

        sleep_min = sleep_scaler.data_min_[0]
        sleep_max = sleep_scaler.data_max_[0]
        predicted_duration = predicted_duration_scaled * (sleep_max - sleep_min) + sleep_min

        recommended_duration = get_sleep_recommendation(predicted_duration)

        return jsonify({
            'success': True,
            'message': 'success',
            'sleep_duration': format_duration(predicted_duration),
            'recommended_sleep_duration': format_duration(recommended_duration)
        })

    except (TypeError, ValueError) as e:
        return jsonify({
            'success': False,
            'message': 'Invalid input: ' + str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=3000)