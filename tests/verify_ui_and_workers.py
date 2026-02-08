import requests
import time
import sys

API_URL = "http://localhost:8000"

def wait_for_api():
    print("Waiting for API to be ready...")
    for _ in range(30):
        try:
            requests.get(API_URL)
            print("API is ready.")
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    print("API failed to start.")
    return False

def verify_thought_fields():
    print("Verifying thought fields...")
    thought_data = {
        "title": "Verification Thought",
        "content": "This is a test thought to verify new fields.",
        "emotions": ["curious"],
        "is_generated": False
    }
    
    try:
        # Create thought
        response = requests.post(f"{API_URL}/thoughts/", json=thought_data)
        response.raise_for_status()
        thought = response.json()
        
        print(f"Created thought: {thought}")
        
        # Check for new fields
        if "action_orientation" not in thought:
            print("ERROR: action_orientation field missing in response.")
            return False
        if "thought_type" not in thought:
            print("ERROR: thought_type field missing in response.")
            return False
            
        print("Fields 'action_orientation' and 'thought_type' are present.")
        return True
    except Exception as e:
        print(f"Error validating thought fields: {e}")
        return False

if __name__ == "__main__":
    if not wait_for_api():
        sys.exit(1)
        
    if verify_thought_fields():
        print("Verification SUCCESS.")
        sys.exit(0)
    else:
        print("Verification FAILED.")
        sys.exit(1)
