from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app)  # ✅ Enables frontend access

@app.route('/process-gps', methods=['POST'])
def process_gps():
    data = request.get_json()
    coords = data['coordinates']

    # Calculate width and length in meters
    width_m = geodesic((coords[0]['lat'], coords[0]['lng']), (coords[1]['lat'], coords[1]['lng'])).meters
    length_m = geodesic((coords[0]['lat'], coords[0]['lng']), (coords[3]['lat'], coords[3]['lng'])).meters

    # Convert to centimeters
    width_cm = int(width_m * 100)
    length_cm = int(length_m * 100)

    # Planting logic
    column_width = 80
    row_spacing = 20

    columns = width_cm // column_width
    rows = length_cm // row_spacing
    seedlings = columns * rows * 4

    return jsonify({
        "width": width_cm,
        "length": length_cm,
        "columns": columns,
        "rows": rows,
        "seedlings": seedlings
    })

if __name__ == '__main__':
    app.run(debug=True)