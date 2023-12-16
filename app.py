from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from fuzzywuzzy import fuzz
import json

app = Flask(__name__, static_url_path='/static')

# Create and train the chatbot
azerothcore_bot = ChatBot('Coral AI')
trainer = ListTrainer(azerothcore_bot)

# Load existing training data for coral reefs from JSON file
try:
    with open('coral_reefs_data.json', 'r') as coral_file:
        coral_data = json.load(coral_file)
        # Train the chatbot with the loaded data
        for item in coral_data:
            input_data = item['input']
            output_data = item['output'] if isinstance(item['output'], list) else [item['output']]
            trainer.train([input_data] + output_data)

except FileNotFoundError as file_not_found_error:
    print(f"Error: {file_not_found_error}")
except json.JSONDecodeError as json_error:
    print(f"Error decoding JSON in coral reefs data file: {json_error}")

# Load existing training data for the team from JSON file
try:
    with open('team_data.json', 'r') as team_file:
        team_data = json.load(team_file)
        # Train the chatbot with the loaded data
        for item in team_data:
            input_data = item['input']
            output_data = item['output'] if isinstance(item['output'], list) else [item['output']]
            trainer.train([input_data] + output_data)

except FileNotFoundError as file_not_found_error:
    print(f"Error: {file_not_found_error}")
except json.JSONDecodeError as json_error:
    print(f"Error decoding JSON in team data file: {json_error}")

# Function for fuzzy matching
def get_best_match(user_input, data):
    max_similarity = 0
    best_responses = []

    try:
        for pair in data:
            question = pair['input']
            similarity = fuzz.ratio(user_input.lower(), question.lower())

            if similarity > max_similarity:
                max_similarity = similarity
                responses = pair['output'] if isinstance(pair['output'], list) else [pair['output']]
                best_responses = responses
            elif similarity == max_similarity:
                responses = pair['output'] if isinstance(pair['output'], list) else [pair['output']]
                best_responses.extend(responses)

    except Exception as e:
        print(f"Error in fuzzy matching: {e}")
        return ["An error occurred in fuzzy matching"]

    return best_responses

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        user_input = request.form.get("user_input")

        # Get the best-matching responses using fuzzy matching
        responses = get_best_match(user_input, coral_data + team_data)

        # Join responses into a single string
        response_text = '' .join(responses)

        return jsonify(response_text)

    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred: {e}")
        return jsonify("An error occurred")


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
