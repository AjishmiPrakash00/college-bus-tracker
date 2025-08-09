from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder="static")

# In-memory store
bus_locations = {}

# Serve static files (HTML, CSS, JS)
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

# API endpoints
@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.json
    bus_locations[data["bus_number"]] = (data["lat"], data["lon"])
    return "Location updated", 200

@app.route("/get_location/<bus_number>")
def get_location(bus_number):
    if bus_number in bus_locations:
        lat, lon = bus_locations[bus_number]
        return jsonify({"lat": lat, "lon": lon})
    return jsonify({"error": "Bus not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
