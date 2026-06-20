import requests
from bs4 import BeautifulSoup
import json

def fetch_live_market_leaders(keyword, country="us", language="en"):
    search_url = f"https://html.duckduckgo.com/html/?q={keyword.replace(' ', '+')}&kl={country}-{language}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a in soup.find_all('a', class_='result__url'):
            url_clean = a.get_text().strip()
            if url_clean and not url_clean.startswith(('http://localhost', 'javascript')):
                if not url_clean.startswith('http'):
                    url_clean = 'https://' + url_clean
                links.append(url_clean)
                if len(links) >= 3:
                    break
        return links
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return []

def extract_structural_blueprint(urls):
    blueprints = {}
    
    for rank, url in enumerate(urls, 1):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                tags_sequence = []
                total_paragraphs = 0
                total_sentences = 0
                
                for tag in soup.find_all(['h1', 'h2', 'h3', 'table', 'ul', 'ol', 'blockquote', 'p']):
                    tags_sequence.append(tag.name.upper())
                    if tag.name == 'p':
                        total_paragraphs += 1
                        total_sentences += len(tag.get_text().split('.'))
                
                avg_sentences_per_p = round(total_sentences / total_paragraphs, 1) if total_paragraphs > 0 else 0
                
                blueprints[f"competitor_rank_{rank}"] = {
                    "url": url,
                    "tag_sequence_flow": tags_sequence[:30],
                    "average_sentences_per_paragraph": avg_sentences_per_p,
                    "uses_tables": "TABLE" in tags_sequence,
                    "uses_bullet_points": "UL" in tags_sequence or "OL" in tags_sequence
                }
        except:
            continue
            
    return blueprints

def generate_ai_writer_manifest(keyword, structural_data):
    manifest = {
        "target_keyword": keyword,
        "governor_status": "SUCCESS",
        "instruction_for_ai_writer": (
            "You must strictly follow the structured sequence decoded from live Google winners. "
            "Replicate header hierarchies (H2, H3), blockquotes, and table positioning as analyzed. "
            "Enforce the exact paragraph density to optimize for the current mobile-first index search intent."
        ),
        "live_seo_blueprint": structural_data
    }
    return json.dumps(manifest, indent=4)

if __name__ == "__main__":

# CHANGE THIS TO YOUR TARGET KEYWORD

KEYWORD_TARGET = "best soccer shoes for ankle support"
    
    top_urls = fetch_live_market_leaders(KEYWORD_TARGET, country="us", language="en")
    raw_seo_rules = extract_structural_blueprint(top_urls)
    buku_aturan_json = generate_ai_writer_manifest(KEYWORD_TARGET, raw_seo_rules)
    
    with open("ai_governor_rules.json", "w", encoding="utf-8") as f:
        f.write(buku_aturan_json)
        
    print(buku_aturan_json)