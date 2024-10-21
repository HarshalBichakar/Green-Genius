# import numpy as np
# import tensorflow as tf
# from flask import Flask, request, jsonify, render_template
# from tensorflow.keras.models import load_model
# from flask_cors import CORS, cross_origin
# from PIL import Image
# import io
# import pandas as pd

# # Load the models
# plant_model = load_model(r'updated_plant_classification_model.h5')
# toxic_model = load_model(r'poison1.h5') # Toxicity model
# other_model = load_model(r'ponp.h5') # Placeholder for other model

# # Class names corresponding to the plant classification model
# class_names = ['aloevera', 'banana', 'bilimbi', 'cantaloupe', 'cassava', 'coconut', 'corn', 'cucumber', 'curcuma', 
#                'eggplant', 'galangal', 'ginger', 'guava', 'kale', 'longbeans', 'mango', 'melon', 'orange', 
#                'paddy', 'papaya', 'peper chili', 'pineapple', 'pomelo', 'shallot', 'soybeans', 'spinach', 
#                'sweet potatoes', 'tobacco', 'waterapple', 'watermelon']

# app = Flask(__name__)
# CORS(app)

# def preprocess_image(file):
#     if file:
#         file_contents = file.read()
#         image = Image.open(io.BytesIO(file_contents))
#         image = image.resize((192, 192))  # Adjust size to match model input
#         img_array = np.array(image, dtype=np.float32)
#         img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#         img_array /= 255.0  # Normalize
#         return img_array

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# @cross_origin()
# def predict():
#     file = request.files['image']
#     img_array = preprocess_image(file)

#     # Predict with plant classification model
#     plant_predictions = plant_model.predict(img_array)
#     plant_class_idx = np.argmax(plant_predictions)
#     plant_label = class_names[plant_class_idx]
    
#     # Fetch plant details from CSV
#     df = pd.read_csv("Details.csv")
#     plant_info = df[df['Plant Name'] == plant_label].to_dict()
    
#     if plant_info:
#         plant_details = {
#             "Plant Name": plant_info['Plant Name'][0],
#             "Biological Name": plant_info['Biological Name'][0],
#             "Medicinal Uses": plant_info['Medicinal Uses'][0],
#             "latitude and longitude": plant_info['latitude and longitude'][0]
#         }
#     else:
#         plant_details = {
#             "Plant Name": "Unknown",
#             "Biological Name": "",
#             "Medicinal Uses": "",
#             "latitude and longitude": ""
#         }

#     # Return JSON response
#     return jsonify({'prediction': plant_details})

# @app.route('/toxic-check', methods=['POST'])
# @cross_origin()
# def toxic_check():
#     file = request.files['image']
#     img_array = preprocess_image(file)

#     # Predict with toxic/non-toxic model
#     toxic_predictions = toxic_model.predict(img_array)
#     toxicity_label = "TOXIC" if np.argmax(toxic_predictions) == 1 else "NON_TOXIC"

#     # Return JSON response
#     return jsonify({"prediction": {"type": toxicity_label}})

# @app.route('/plant-details')
# @cross_origin()
# def fetchPlantDetails():
#     df = pd.read_csv('Details.csv')
#     locations = []

#     for i in df.index:
#         plant_name = df.loc[i, 'Plant Name']
#         if plant_name == '':  # Skip specific plant if needed
#             continue

#         lat_long_str = df.loc[i, 'latitude and longitude']
#         lat_long_list = lat_long_str.strip('[]').split(',')
#         lat, long = float(lat_long_list[0]), float(lat_long_list[1])

#         plant_info = {
#             'name': plant_name,
#             'points': [{'lat': lat, 'long': long}]
#         }
#         locations.append(plant_info)

#     return jsonify({'data': locations})

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=5000)
