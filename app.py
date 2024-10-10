from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

Kora_url = "https://nexus-ai-30oy.onrender.com/Nex?query={}"
Sman_url = "http://3.27.248.76:3000/generate-image-flux?prompt={}"

# Single route handling both image generation and user messages
@app.route('/process', methods=['GET','POST'])
def process_request():
    user_input = request.args.get('query')
    
    if not user_input:
        return jsonify({"error": "No query provided"}), 400

    # Check if the input is for image generation (starts with 'Imagine,')
    if user_input.startswith('Imagine'):
        prompt = user_input.split('Imagine', 1)[1].strip()

        # Request to generate an image URL
        image_api_url = Sman_url.format(prompt=prompt)
        response = requests.get(image_api_url)

        if response.status_code == 200:
            # Assuming the response is a JSON containing the image URL
            image_data = response.json()
            image_url = image_data.get("image_url")  # Adjust based on the API's JSON structure
            
            if image_url:
                return jsonify({"image_url": image_url})
            else:
                return jsonify({"error": "No image Created"}), 500
        else:
            return jsonify({"error": "Failed to retrieve image URL"}), response.status_code

    else:
        # If it's a normal user message, call the Kora API
        kora_response = requests.get(Kora_url.format(user_input))
        
        if kora_response.status_code == 200:
            return jsonify(kora_response.json())
        else:
            return jsonify({"error": "Failed to retrieve message"}), kora_response.status_code

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)
