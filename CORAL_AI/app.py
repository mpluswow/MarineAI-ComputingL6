# Import necessary libraries and modules
from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from fuzzywuzzy import fuzz
import json

# Create a Flask application
app = Flask(__name__, static_url_path='/static')

# Create a ChatBot instance named 'Coral AI'
azerothcore_bot = ChatBot('Coral AI')

# Create a trainer for the chatbot
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
    # Print an error message if the file is not found
    print(f"Error: {file_not_found_error}")

except json.JSONDecodeError as json_error:
    # Print an error message if there's an issue decoding JSON
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
    # Print an error message if the file is not found
    print(f"Error: {file_not_found_error}")

except json.JSONDecodeError as json_error:
    # Print an error message if there's an issue decoding JSON
    print(f"Error decoding JSON in team data file: {json_error}")

# Function for fuzzy matching
def get_best_match(user_input, data):
    max_similarity = 0
    best_responses = []

    try:
        # Iterate through the data for fuzzy matching
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
        # Print an error message if there's an issue with fuzzy matching
        print(f"Error in fuzzy matching: {e}")
        return ["An error occurred in fuzzy matching"]

    return best_responses

# Route for the home page
@app.route("/")
def home():
    return render_template("index.html")

# Route for handling user input and getting chatbot responses
@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        # Get user input from the form
        user_input = request.form.get("user_input")

        # Get the best-matching responses using fuzzy matching
        responses = get_best_match(user_input, coral_data + team_data)

        # Join responses into a single string
        response_text = ' '.join(responses)

        # Log user interaction
        log_interaction(user_input, responses)

        # Return the chatbot response as JSON
        return jsonify(response_text)

    except Exception as e:
        # Log and return an error message if an exception occurs
        print(f"An error occurred: {e}")
        return jsonify("An error occurred")

# Function to log user interactions to a file

def log_interaction(user_input, bot_responses):
    with open('interaction_log.txt', 'a') as log_file:
        log_file.write(f'[Q] {user_input}\n')
        log_file.write(f'[A] {" ".join(bot_responses)}\n')


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
