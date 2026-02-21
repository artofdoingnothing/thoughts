import requests
from bs4 import BeautifulSoup
import random
import time
import sys
import argparse
from urllib.parse import urljoin, urlparse

# Base API URL
API_URL = "http://localhost:8000"

def get_persona_id(name):
    """Find persona ID by name or create a new one."""
    print(f"Checking for persona: {name}")
    try:
        response = requests.get(f"{API_URL}/personas/")
        response.raise_for_status()
        personas = response.json()
        
        for p in personas:
            if p['name'].lower() == name.lower():
                return p['id']
                
        # Create new if not found
        print(f"Persona '{name}' not found. Creating new persona...")
        response = requests.post(f"{API_URL}/personas/", json={
            "name": name,
            "age": random.randint(20, 60),
            "gender": random.choice(["Male", "Female", "Non-binary"]),
            "additional_info": {"notes": "Auto-created by script"}
        })
        response.raise_for_status()
        return response.json()['id']
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with API: {e}")
        sys.exit(1)

def scrape_essay_urls(base_url):
    """Scrapes essay URLs from the base URL."""
    print(f"Scraping URLs from {base_url}...")
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        
        # Look for any link that contains 'essay' or is in an 'essays' section
        # We also check the text of the link
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text().lower()
            full_url = urljoin(base_url, href)
            
            # Normalize URL (remove fragment)
            full_url = full_url.split('#')[0]
            
            # Filter: must be within the same domain
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                if 'essay' in full_url.lower() or 'essay' in text:
                    # Avoid the base essays page itself if it's just a list
                    if full_url.rstrip('/') != base_url.rstrip('/'):
                        links.add(full_url)
        
        # If no 'essay' links found, look for more generic article patterns
        if not links:
            print("Warning: No links containing 'essay' found. Looking for common blog/article patterns...")
            for a in soup.find_all('a', href=True):
                href = a['href']
                full_url = urljoin(base_url, href).split('#')[0]
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    path = urlparse(full_url).path
                    # Heuristic: paths with multiple segments are often articles
                    if len(path.strip('/').split('/')) >= 2:
                        links.add(full_url)
                        
        return list(links)
    except Exception as e:
        print(f"Error scraping {base_url}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Trigger thought generation for random essay URLs.")
    parser.add_argument("--url", help="The base URL to scrape essays from")
    parser.add_argument("--persona", help="The name of the persona to associate with thoughts")
    
    args = parser.parse_args()
    
    url = args.url
    persona_name = args.persona
    
    if not url:
        url = input("Enter the URL to scrape (e.g., https://paulgraham.com/articles.html): ").strip()
    if not persona_name:
        persona_name = input("Enter the persona name (e.g., Paul): ").strip()
        
    if not url or not persona_name:
        print("Both URL and persona name are required.")
        sys.exit(1)
    
    persona_id = get_persona_id(persona_name)
    print(f"Using Persona ID: {persona_id}")
    
    all_urls = scrape_essay_urls(url)
    print(f"Found {len(all_urls)} potential URLs.")
    
    if not all_urls:
        print("No URLs found to process. Exiting.")
        return
        
    # Pick 50 random URLs (or all if less than 50)
    num_to_pick = min(50, len(all_urls))
    selected_urls = random.sample(all_urls, num_to_pick)
    print(f"Selected {len(selected_urls)} random URLs for processing.")
    
    # Process in batches of 5 every 10 seconds
    batch_size = 5
    for i in range(0, len(selected_urls), batch_size):
        batch = selected_urls[i : i + batch_size]
        print(f"\nTriggering batch {i//batch_size + 1}:")
        for b_url in batch:
            print(f"  - {b_url}")
        
        try:
            response = requests.post(f"{API_URL}/generate-thoughts/", json={
                "urls": batch,
                "persona_id": persona_id
            })
            
            if response.status_code == 200:
                print(f"Status: Success - {response.json().get('message')}")
            else:
                print(f"Status: Failed - {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Status: Error - {e}")
            
        if i + batch_size < len(selected_urls):
            print("Next batch in 10 seconds...")
            time.sleep(10)
            
    print("\nAll tasks scheduled successfully.")

if __name__ == "__main__":
    main()
