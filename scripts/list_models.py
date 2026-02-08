import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Use the one from .env if running locally without docker
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

print(f"Using API Key: {api_key[:5]}...")

try:
    client = genai.Client(api_key=api_key)
    print("Fetching models...")
    # New SDK listing
    # Note: google-genai SDK usage for listing models might be different
    # attempting based on documentation patterns
    
    # Try generic listing if possible or just try to generate with a known working model
    # Client.models.list() might not be straightforward in new SDK 0.x?
    # Let's try to verify if it works at all.
    
    # Actually, let's just try to print what we can regarding models.
    # The SDK is new, documentation is key.
    # Assuming standard pattern:
    
    # If using google-genai, the client has .models
    
    # Let's try to call list_models
    for m in client.models.list():
        print(f"Model: {m.name} - {m.display_name}")

except Exception as e:
    print(f"Error with google-genai: {e}")
    
    # Fallback to old SDK just to see if it works if installed (it shouldn't be)
    try:
        import google.generativeai as old_genai
        old_genai.configure(api_key=api_key)
        for m in old_genai.list_models():
            print(f"Old SDK Model: {m.name}")
    except ImportError:
        pass
    except Exception as e2:
        print(f"Error with old SDK: {e2}")
