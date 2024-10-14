from flask import Flask, request, jsonify, Response
import requests
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

Kora_url = "https://kora-ai-sh1p.onrender.com/koraai?query={}"
Sman_url = "https://3.27.248.76:3000/generate-image-flux?prompt={}"

# Single route handling both image generation and user messages
@app.route('/process', methods=['GET'])
def process_request():
    user_input = request.args.get('query')
    
    if not user_input:
        return jsonify({"error": "No query provided"}), 400

    # Check if the input is for image generation (starts with 'Imagine,')
    if user_input.startswith('Imagine,'):
        prompt = user_input.split('Imagine,', 1)[1].strip()

        # Create the correct URL for the image generation API
        image_api_url = Sman_url.format(prompt)

        # Make the request to the image generation API
        response = requests.get(image_api_url)

        if response.status_code == 200:
            # Simply pass through the response content from the image API
            return Response(response.content, content_type=response.headers.get('Content-Type'))
        else:
            return jsonify({"error": f"Failed to retrieve image: {response.status_code}"}), response.status_code

    else:
        # If it's a normal user message, call the Kora API
        kora_response = requests.get(Kora_url.format(user_input))
        
        if kora_response.status_code == 200:
            return jsonify(kora_response.json())
        else:
            return jsonify({"error": "Failed to retrieve message"}), kora_response.status_code

if __name__ == '__main__':
    app.run(debug=True)
