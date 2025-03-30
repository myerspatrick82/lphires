from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/start-scraping", methods=["POST"])
def start_scraping():
    data = request.get_json()
    field = data.get("field")

    if not field:
        return jsonify({"error": "No career field provided"}), 400

    # Call scraper.py with the career field as an argument
    subprocess.Popen(["python", "src/scraper.py", field])

    return jsonify({"message": "Scraper started"}), 200

@app.route('/part-one')
def part_one():
    return render_template('PartOne.html')

if __name__ == "__main__":
    app.run(debug=True)
