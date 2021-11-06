import hashlib
from flask import Flask, send_from_directory, render_template, request, jsonify
from threading import Thread
import os

app = Flask('')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET')

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

    if password == hashlib.sha3_512(os.getenv("IMAGE_API_PASSWORD").encode()).hexdigest():
        print('gud')
    else:
        print('oop')

    raise NotImplementedError("Development of the image API is an ongoing effort.")

def run(debug=False):
    if debug:
        app.run(port=8080, debug=False)
    else:
        app.run(host="0.0.0.0", port=8080, debug=False)

def run_site():
    server = Thread(target=run)
    server.start()
