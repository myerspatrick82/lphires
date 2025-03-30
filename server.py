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

    try:
        # Step 1: Scrape data based on career field
        subprocess.run(["python", "src/scraper.py", field], check=True)

        # Step 2: Run summarization on the result
        subprocess.run(["python", "src/summarization.py"], check=True)

        return jsonify({"message": "Pipeline completed!"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Pipeline failed: {str(e)}"}), 500

@app.route('/part-one')
def part_one():
    return render_template('PartOne.html')

@app.route('/calculate-similarities', methods=["POST"])
def calculate_similarities():
    try:
        subprocess.run(["python", "src/similarities.py"], check=True)
        return jsonify({"success": True})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": str(e)})
    
import json

@app.route('/progress')
def get_progress():
    try:
        with open("progress.json") as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"scraping": 0, "summarizing": 0})


@app.route('/box')
def box():
    return render_template('Box.html')


if __name__ == "__main__":
    app.run(debug=True)
