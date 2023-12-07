# app.py -----------------------------------------------------------
from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
import os
from app.model_loader import load_model, predict_image
from bson.binary import Binary
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client.get_database('inventory')
inventory_collection = db['inventory']

model = load_model()  # Cargar el modelo al inicio de la aplicación

def uploadImage(name):
    with open(name, "rb") as file:
        encoded = Binary(file.read())
    inventory_collection.insert_one({"image": encoded})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST', 'GET'])
def create():
    if 'file' not in request.files:
        return render_template('index.html', message='No file part')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', message='No selected file')

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.root_path, 'static/files', filename)
        file.save(file_path)

        # Realizar la predicción con el modelo
        predictions = predict_image(model, file_path)

        # Subir la imagen a MongoDB
        uploadImage(file_path)

        # Obtener la URL de la imagen
        image_url = url_for('static', filename=f'files/{filename}')

        # Pasar el mensaje de éxito, la URL de la imagen y las predicciones al template
        return render_template('index.html', message='Image Uploaded Successfully!!', image_url=image_url, predictions=predictions)
        print("Predictions:", predictions)


    except Exception as e:
        # Pasar un mensaje de error al template
        return render_template('index.html', message=f'Image Upload Failed: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
