from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
from collections import Counter
import re

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from other origins (like your frontend)

@app.route('/')
def home():
    return "Flask server is running!"

# Function to process text and find the top N frequent words
def get_top_frequent_words(text, n=10):
    # Convert text to lowercase and find all words, including those with hyphens or apostrophes
    words = re.findall(r'\b\w+\b', text.lower())


    print("Extracted Words:", words)  # Debug print to verify words

    # Count word frequencies
    word_counts = Counter(words)

    # Get the top N most common words
    top_words = word_counts.most_common(n)
    return [{'word': word, 'count': count} for word, count in top_words]

# REST API endpoint to accept URL and return top frequent words
@app.route('/api/top-words', methods=['POST'])
def top_words():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        # Fetch and parse the webpage
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the text content
        text = soup.get_text(separator=' ', strip=True)
        
        print("Extracted Text:", text)  # Debug print to verify the raw text
        
        # Get top words
        top_words = get_top_frequent_words(text, 10)
        return jsonify(top_words)
    
    except Exception as e:
        print("Error fetching URL:", e)  # Additional error logging
        return jsonify({"error": "Failed to fetch the URL"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
