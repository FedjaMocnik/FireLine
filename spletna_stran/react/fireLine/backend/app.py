from flask import Flask, send_from_directory, jsonify
import os
import time
#from your_function_file import generate_image  # Import your image function

app = Flask(__name__, static_folder="../public", static_url_path="/public")

@app.route("/generate", methods=["POST"])
def generate():
    time.sleep(3)
    #generate_image()  # Your function that creates img.png
    return jsonify({"success": True})

@app.route("/public/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)