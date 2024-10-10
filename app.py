from flask import Flask, request, jsonify, send_file
import requests
from io import BytesIO

app = Flask(__name__)

Kora_url = "https://kora-ai.onrender.com/koraai?query={}"
Sman_url = "https://example.com?prompt={}"

# Single route handling both image generation and user messages
@app.route('/process', methods=['GET'])
def process_request():
    user_input = request.args.get('query')
    
    if not user_input:
        return jsonify({"error": "No query provided"}), 400

    # Check if the input is for image generation (starts with 'Imagine,')
    if user_input.startswith('Imagine,'):
        prompt = user_input.split('Imagine,', 1)[1].strip()

        # Request to generate an image
        image_url = Sman_url.format(prompt=prompt)
        response = requests.get(image_url)

        if response.status_code == 200:
            # Handle and send back the image
            image = BytesIO(response.content)
            return send_file(image, mimetype='image/jpeg')
        else:
            return jsonify({"error": "Failed to retrieve image"}), response.status_code

    else:
        # If it's a normal user message, call the Kora API
        kora_response = requests.get(Kora_url.format(user_input))
        
        if kora_response.status_code == 200:
            return jsonify(kora_response.json())
        else:
            return jsonify({"error": "Failed to retrieve message"}), kora_response.status_code

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)
