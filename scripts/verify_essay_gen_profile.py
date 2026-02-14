import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def create_persona(name, age, gender):
    response = requests.post(f"{BASE_URL}/personas/", json={"name": name, "age": age, "gender": gender})
    response.raise_for_status()
    return response.json()

def create_thought(persona_id, content):
    response = requests.post(f"{BASE_URL}/thoughts/", json={"content": content, "persona_id": persona_id})
    response.raise_for_status()
    return response.json()

def derive_persona(source_persona_id, adjective, percentage):
    response = requests.post(f"{BASE_URL}/personas/derive", json={
        "source_persona_id": source_persona_id,
        "name_adjective": adjective,
        "percentage": percentage
    })
    response.raise_for_status()
    return response.json()

def generate_essay(persona_id, starting_text):
    response = requests.post(f"{BASE_URL}/essay/generate", json={
        "persona_id": persona_id,
        "starting_text": starting_text
    })
    response.raise_for_status()
    return response.json()

def get_job_status(job_id):
    response = requests.get(f"{BASE_URL}/essay/status/{job_id}")
    response.raise_for_status()
    return response.json()

def main():
    print("1. Creating Source Persona...")
    source_persona = create_persona("Writer", 40, "Non-binary")
    print(f"Source Persona ID: {source_persona['id']}")

    print("2. Adding Thoughts...")
    thoughts = [
        "I feel overwhelming joy when I see the sunrise. It reminds me of new beginnings.",
        "Sometimes sadness creeps in like a fog, obscuring my clarity.",
        "Anxiety is a constant hum in the background of my life.",
        "Peace is found in the quiet moments of the night."
    ]
    for t in thoughts:
        create_thought(source_persona['id'], t)

    print("3. Deriving Persona (to get a profile)...")
    # Wait a bit for thoughts to be processed if needed, but here we just need them in DB for derivation
    time.sleep(2) 
    derived_persona = derive_persona(source_persona['id'], "Emotional", 100)
    print(f"Derived Persona ID: {derived_persona['id']}")
    print(f"Derived Persona Profile: {derived_persona.get('profile')}")

    if not derived_persona.get('profile'):
        print("Error: Derived persona has no profile!")
        sys.exit(1)

    print("4. Generating Essay with Derived Persona...")
    job_data = generate_essay(derived_persona['id'], "The storm raged on.")
    job_id = job_data['job_id']
    print(f"Job ID: {job_id}")

    print("5. Polling for completion...")
    for _ in range(30):
        status_data = get_job_status(job_id)
        status = status_data['status']
        print(f"Status: {status}")
        
        if status == 'finished':
            print("Essay Generation Successful!")
            print(f"Result: {status_data['result']}")
            # Ideally we check logs to see if it used the profile path, but success here is a good sign.
            break
        elif status == 'failed':
            print(f"Job Failed: {status_data.get('error')}")
            sys.exit(1)
        
        time.sleep(2)
    else:
        print("Timeout waiting for job completion.")
        sys.exit(1)

if __name__ == "__main__":
    main()
