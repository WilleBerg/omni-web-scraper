import requests
from bs4 import BeautifulSoup

from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This allows cross-origin requests

@app.route('/get-data', methods=['GET'])
def get_data():
    # This is where you put your Python code that generates JSON    
    return jsonify(scrape_omni_news())



def scrape_omni_news():
    # URL of the website to scrape
    url = "https://omni.se/senaste"  # Assuming this is the website based on the filename
    
    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        # Send a GET request to the website
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all h2 elements
            h2_elements = soup.find_all('h2')
            
            # Create a list to store the articles
            articles = []
            
            # For each h2 element, find the next p element
            for h2 in h2_elements:
                title = h2.text.strip()
                
                # Find the next p element after the h2
                p_element = h2.find_next('p')
                
                # If a p element is found, get its text
                if p_element:
                    paragraph = p_element.text.strip()
                else:
                    paragraph = "No paragraph found"
                
                # Add the title and paragraph to the articles list
                articles.append({
                    'title': title,
                    'paragraph': paragraph
                })
            
            return articles
        else:
            print(f"Failed to retrieve the website. Status code: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_to_json(articles, filename='news_articles.json'):
    import json

    """Save the scraped articles to a CSV file."""
    if not articles:
        print("No articles to save.")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            file.write(json.dumps(articles))
        print(f"Successfully saved {len(articles)} articles to {filename}")
    except Exception as e:
        print(f"Failed to save articles to JSON: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
