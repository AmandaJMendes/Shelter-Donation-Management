from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='.')

# Serve static files from the "dist" directory
@app.route('/')
@app.route('/<path:path>')
def serve(path=''):
    if path and '.' in path:
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'home.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)