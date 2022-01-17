import hashlib
from flask import Flask, send_from_directory, render_template, request, jsonify
from werkzeug.utils import secure_filename
from threading import Thread
from pathlib import Path
import os

CURRENT_PATH = Path(__file__).parent.absolute()
TEMPLATE_FOLDER = Path.joinpath(CURRENT_PATH, "templates")
ALLOWED_EXTENSIONS = {
    "png" # png has an alpha channel
}

app = Flask('', template_folder=TEMPLATE_FOLDER)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET'].encode("latin-1")
app.config['UPLOAD_FOLDER'] = Path.joinpath(CURRENT_PATH, 'media')

def get_resource_path(resource_type: str, resource: str):
    """Utility function to get absolute filenames"""
    if resource_type == "image":
        return os.path.join(app.config['UPLOAD_FOLDER'], resource)
    else:
        raise NotImplementedError


def validate_imagename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main():
    return render_template("home.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/upload-image', methods=['POST'])
def upload_image():
    """Takes in 2 multipart form data parameters.

    password - An API password hashed with sha3-512, just makes sure that the API is only internally used.
    
    image - An image."""
    password = request.form.to_dict()['password']
    image = request.files['image']

    if password == hashlib.sha3_512(os.environ["IMAGE_API_PASSWORD"].encode()).hexdigest():
        if validate_imagename(image.filename):
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
            return "Success!", 200
        else:
            return "Invalid Filename", 400
    else:
        return "Invalid Password", 400

def run(debug):
    if debug:
        app.run(port=8080, debug=True)
    else:
        app.run(host="0.0.0.0", port=8080, debug=False)

def run_site(debug):
    server = Thread(target=lambda debug=debug: run(debug))
    server.start()
