import os
import requests
from bs4 import BeautifulSoup
from libs.llm_service.gemini import GeminiLLM
from libs.processor_service.prompts import THOUGHT_GENERATION_PROMPT

def debug_llm(url):
    print(f"Fetching {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    text_content = "\n".join(paragraphs)
    if len(text_content) < 100:
        text_content = soup.get_text()
    
    print(f"Content length: {len(text_content)}")
    
    print("Initializing LLM...")
    llm = GeminiLLM() # Uses env GEMINI_API_KEY
    
    prompt = THOUGHT_GENERATION_PROMPT.format(blog_content=text_content)
    
    print("Generating content...")
    try:
        response_text = llm.generate_content(prompt)
        print("--- RAW RESPONSE ---")
        print(response_text)
        print("--- END RAW RESPONSE ---")
        print(f"Response length: {len(response_text)}")
        print(f"Response repr: {repr(response_text)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_llm("https://nagekar.com/2025/08/parasocial-relationships.html")
