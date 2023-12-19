import json

def create_json_from_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = []
    current_input = ""
    current_output = ""

    for line in lines:
        line = line.strip()

        if line.startswith("[Q]"):
            if current_input:
                data.append({"input": current_input, "output": current_output})
            current_input = line[4:].strip()
            current_output = ""
        elif line.startswith("[A]"):
            current_output += line[4:].strip()
    
    # Add the last pair
    if current_input:
        data.append({"input": current_input, "output": current_output})

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2)

if __name__ == "__main__":
    input_text_file = "data_to_read.txt"  # Replace with your input text file
    output_json_file = "readed_data.json"  # Replace with the desired output JSON file

    create_json_from_text(input_text_file, output_json_file)
