import requests
from bs4 import BeautifulSoup

from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify(scrape_omni_news())



def scrape_omni_news():
    url = "https://omni.se/senaste"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            h2_elements = soup.find_all('h2')
            
            articles = []
            
            for h2 in h2_elements:
                is_ad = False
                
                parent = h2.parent
                for _ in range(7):
                    if parent is None:
                        break
                    
                    ad_spans = parent.find_all('span', string=lambda text: text and "ANNONS" in text)
                    # print(ad_spans,i, h2.text)
                    if ad_spans:
                        is_ad = True
                        break
                    
                    parent = parent.parent
                
                if is_ad:
                    continue
                title = h2.text.strip()
                
                p_element = h2.find_next('p')
                
                
                if p_element:
                    paragraph = p_element.text.strip()
                else:
                    paragraph = "No paragraph found"
                
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
