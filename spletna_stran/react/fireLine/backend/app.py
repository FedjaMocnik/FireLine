from flask import Flask, send_from_directory, jsonify, request
import os


#from your_function_file import generate_image  # Import your image function

app = Flask(__name__, static_folder="../public", static_url_path="/public")

@app.route("/generate", methods=["POST"])
def generate():
    import sys
    import os

    # Get the absolute path to the directory containing main.py
    main_dir = os.path.abspath(os.path.join(__file__, "../../../../..", "./"))
    #print("Resolved main_dir path:", main_dir)
    #print("Files in main_dir:", os.listdir(main_dir))
    # Add it to sys.path
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)

    # Change current working directory if your code relies on relative paths
    os.chdir(main_dir)

    # Now you can safely import and call main.py as a module
    from main import generate  # or from main import some_function
    data = request.get_json()
    coords = data.get("coordinates")
    print("Received coordinates:", coords)
    c = generate(coords)
    #generate_image()  # Your function that creates img.png
    return jsonify({"success": True})

@app.route("/public/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)