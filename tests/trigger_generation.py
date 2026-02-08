import requests
import time

API_URL = "http://localhost:8000"

def trigger_generation():
    print("Triggering generation...")
    # First get a persona or create one
    personas = requests.get(f"{API_URL}/personas/").json()
    if not personas:
        p = requests.post(f"{API_URL}/personas/", json={"name": "Test Persona", "age": 30, "gender": "Non-binary"}).json()
        persona_id = p['id']
    else:
        persona_id = personas[0]['id']

    # Use a dummy URL or a real one. The worker fetches it. 
    # If network is restricted in worker, this might fail.
    # Assuming worker has internet.
    # I'll use a simple text page or example.com
    url = "https://example.com" 
    
    payload = {
        "urls": [url],
        "persona_id": persona_id
    }
    
    resp = requests.post(f"{API_URL}/generate-thoughts/", json=payload)
    print(resp.json())

if __name__ == "__main__":
    trigger_generation()
