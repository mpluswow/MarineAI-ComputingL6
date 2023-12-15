from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from fuzzywuzzy import fuzz
import json

app = Flask(__name__)

# Create and train the chatbot
azerothcore_bot = ChatBot('Coral AI')
trainer = ListTrainer(azerothcore_bot)

# Load training data from JSON file
try:
    with open('training_data.json', 'r') as file:
        training_data = json.load(file)

        # Train the chatbot with the loaded data
        for item in training_data:
            trainer.train([item['input'], item['output']])

except FileNotFoundError as file_not_found_error:
    print(f"Error: {file_not_found_error}")
except json.JSONDecodeError as json_error:
    print(f"Error decoding JSON in training data file: {json_error}")

# Function for fuzzy matching
def get_best_match(user_input, training_data):
    max_similarity = 0
    best_response = ""

    for pair in training_data:
        question = pair['input']
        similarity = fuzz.ratio(user_input.lower(), question.lower())

        if similarity > max_similarity:
            max_similarity = similarity
            best_response = pair['output']

    return best_response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form.get("user_input")

    # Get the best-matching response using fuzzy matching
    response = get_best_match(user_input, training_data)

    return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

