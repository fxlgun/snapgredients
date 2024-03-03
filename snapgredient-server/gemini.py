import requests
import json

def askgemini(prompt):
    GENERATE_CONTENT_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent?key=AIzaSyAtQJG86qdIVOXbJt9c8JCeSgIydIOmJ0g"
    
    # Keep the configuration from your file
    generation_config = {
        "temperature": 0,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 10000,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
    ]

    request_body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": generation_config,
        "safetySettings": safety_settings
    }

    response = requests.post(GENERATE_CONTENT_URL, json=request_body)

    if response.status_code == 200:
        data = response.json()
        # Extracting the response content
        # Assuming there is only one content in the response for simplicity
        newData = data['candidates'][0]['content']['parts'][0]['text']
        return newData
    else:
        return f"Error: {response.status_code}"


