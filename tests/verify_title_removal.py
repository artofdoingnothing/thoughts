import requests
import time

API_URL = "http://localhost:8000"

def test_create_thought_no_title():
    print("Testing Create Thought (No Title)...")
    payload = {
        "content": "This is a thought without a title. It should persist.",
        "emotions": ["Hopeful"]
    }
    try:
        response = requests.post(f"{API_URL}/thoughts/", json=payload)
        response.raise_for_status()
        data = response.json()
        print(f"Success! Created thought ID: {data['id']}")
        if 'title' in data:
            print("FAILURE: Title field still present in response!")
            return False
        else:
            print("Success: Title field absent from response.")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_list_thoughts():
    print("Testing List Thoughts...")
    try:
        response = requests.get(f"{API_URL}/thoughts/")
        response.raise_for_status()
        items = response.json()['items']
        if items:
            print(f"Retrieved {len(items)} thoughts.")
            first_item = items[0]
            if 'title' in first_item:
                print("FAILURE: Title field still in list response!")
                return False
            else:
                 print("Success: Title field absent from list response.")
                 return True
        else:
            print("No thoughts to check.")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Waiting for API to be ready...")
    time.sleep(5)
    if test_create_thought_no_title() and test_list_thoughts():
        print("ALL TESTS PASSED")
    else:
        print("TESTS FAILED")
