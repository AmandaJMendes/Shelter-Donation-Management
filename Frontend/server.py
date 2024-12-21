from flask import Flask, send_from_directory

app = Flask(__name__, static_folder=".")


# Serve static files from the "Frontend" directory
@app.route("/")
@app.route("/<path:path>")
def serve(path=""):
    if path and "." in path:
        print(path)
        return send_from_directory(app.static_folder, path)
    return send_from_directory(
        app.static_folder, "home.html"
    )  # Alterei para a 'home', pois entendi que os users terão acesso a ela mesmo não logados. TODO: cria botão de login


if __name__ == "__main__":
    app.run(debug=True, port=3000)
