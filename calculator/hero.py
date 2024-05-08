from flask import Flask, jsonify
import requests
import time
from collections import deque

app = Flask(__name__)

window_size = 10
numbers_window = deque(maxlen=window_size)
average = 0

def fetch_numbers():
    # Fetch numbers from the third-party server
    response = requests.get("https://api.testserver.com/numbers")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def calculate_average():
    return sum(numbers_window) / len(numbers_window)

def update_window(new_numbers):
    for num in new_numbers:
        if num not in numbers_window:
            numbers_window.append(num)

@app.route("/numbers/<numberid>")
def process_request(numberid):
    global numbers_window
    global average

    start_time = time.time()

    new_numbers = fetch_numbers()
    if new_numbers is None:
        return jsonify({"error": "Failed to fetch numbers"}), 500

    update_window(new_numbers)
    average = calculate_average()

    end_time = time.time()

    response_data = {
        "windowPrevState": list(numbers_window),
        "windowCurrState": list(numbers_window),
        "numbers": new_numbers,
        "avg": round(average, 2)
    }

    return jsonify(response_data)

if __name__ == "_main_":
    app.run()