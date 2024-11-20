from flask import Flask, send_from_directory

app = Flask(__name__, static_folder=".")

@app.route('/')
def serve_index():
    """
    Sirve la página principal del frontend.
    """
    return send_from_directory(app.static_folder, "index.html")

@app.route('/<path:path>')
def serve_static_files(path):
    """
    Sirve archivos estáticos como CSS, JS o imágenes.
    """
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
