#main.py -----------------------------------------------------------
import os
from flask import Flask
from app.routes import app as application

if __name__ == '__main__':
    templates_path = os.path.join(application.root_path, 'templates')
    print(f"La ruta de las plantillas es: {templates_path}")
    application.run(debug=True)
