from flask import Flask, send_from_directory, jsonify, request
import os

app = Flask(__name__, static_folder="../public", static_url_path="/public")

@app.route("/generate", methods=["POST"])
def generate():
    import sys
    import os

    # Get the absolute path to the directory containing main.py
    main_dir = os.path.abspath(os.path.join(__file__, "../../../../..", "./"))
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)
    os.chdir(main_dir)

    from main import generate
    data = request.get_json()
    coords = data.get("coordinates")
    date = data.get("date") 
    print("Received coordinates:", coords)
    print("Received date:", date)
    faktor_izboljsave = generate(coords,date) 
    
    return jsonify({"success": True, "faktor_izboljsave" : faktor_izboljsave})

@app.route("/public/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)