# model_loader.py
import os
import tensorflow as tf
from app.image_utils import preprocess_image

model_path = os.path.join(os.path.dirname(__file__), 'model', 'Fruits360.h5')
model = tf.keras.models.load_model(model_path)
print(model.summary())

source_folder = os.path.join(os.path.dirname(__file__), 'model', 'test')
categories = os.listdir(source_folder)
categories.sort()
numOfClasses = len(categories)
print(categories)

def predict_image(image_path):
    processed_image = preprocess_image(image_path)
    predictions = model.predict(processed_image)
    # Devolver la categoría predicha en lugar de las probabilidades
    predicted_category = categories[tf.argmax(predictions, axis=1).numpy()[0]]
    return predicted_category
