# routes.py
from flask import render_template, url_for, request
from werkzeug.utils import secure_filename
from app import app
from app.model_loader import predict_image, categories
from app.model_utils import uploadImage, get_latest_uploaded_image_path
from app.image_utils import preprocess_image
import os

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

        # Subir la imagen a MongoDB
        uploadImage(file_path)

        # Realizar la predicción con el modelo
        predicted_category = predict_image(file_path)

        # Obtener la URL de la imagen
        image_url = url_for('static', filename=f'files/{filename}')

        # Pasar el mensaje de éxito, la URL de la imagen y la predicción al template
        return render_template('index.html', message='Image Uploaded Successfully!!', image_url=image_url, predictions=predicted_category)

    except Exception as e:
        # Pasar un mensaje de error al template
        return render_template('index.html', message=f'Image Upload Failed: {str(e)}')
    
@app.route('/test_latest', methods=['GET'])
def test_latest():
    # Obtener la carpeta 'static/files'
    files_folder = os.path.join(app.root_path, 'static/files')

    # Obtener la última imagen subida desde la carpeta 'static/files'
    latest_image_path = get_latest_uploaded_image_path(files_folder)

    # Realizar la predicción con el modelo
    predicted_category = predict_image(latest_image_path)

    # Obtener el contenido actual de la página
    existing_content = obtener_contenido_existente()

    # Resto del código para imprimir resultados
    return render_template('index.html', message='Image Uploaded Successfully!!', image_url=url_for('static', filename=f'files/{filename}'), predictions=predicted_category, existing_content=existing_content)

def obtener_contenido_existente():
    # Función ficticia para obtener el contenido existente, ajusta según tu caso
    # Por ejemplo, puedes recuperar datos de la base de datos o cualquier otra fuente de información
    return "Contenido existente aquí"
