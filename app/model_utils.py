# model_utils.py

from bson.binary import Binary
import os
import pymongo
from app import inventory_collection
from app.model_loader import predict_image  # Agregado para obtener la predicción

def uploadImage(name):
    with open(name, "rb") as file:
        encoded = Binary(file.read())

    # Obtener el nombre y la extensión de la imagen
    nombre, extension = obtener_nombre_y_extension(name)

    # Realizar la predicción con el modelo
    prediction = predict_image(name)

    # Crear un documento con los datos de la imagen, nombre, extensión y la predicción
    documento = {
        'nombre': nombre,
        'extension': extension,
        'image': encoded,
        'prediction': prediction  # Agregar la predicción aquí
    }

    # Insertar el documento en la colección de MongoDB
    inventory_collection.insert_one(documento)

def obtener_nombre_y_extension(ruta):
    # Obtener el nombre y la extensión de la imagen a partir de la ruta
    nombre_con_extension = os.path.basename(ruta)
    nombre, extension = os.path.splitext(nombre_con_extension)
    return nombre, extension[1:]  # Eliminar el punto inicial en la extensión

def get_latest_uploaded_image_path(files_folder):
    try:
        # Consultar MongoDB para obtener el documento más reciente
        latest_document = inventory_collection.find_one(sort=[('_id', pymongo.DESCENDING)])

        if latest_document:
            # Obtener el nombre y la extensión desde el documento
            nombre = latest_document.get('nombre', '')
            extension = latest_document.get('extension', '')

            # Construir la ruta completa
            latest_image_path = os.path.join(files_folder, f"{nombre}.{extension}")

            return latest_image_path
        else:
            print("No hay documentos en la colección.")
            return None
    except Exception as e:
        print(f"Error getting latest image path: {str(e)}")
        return None
