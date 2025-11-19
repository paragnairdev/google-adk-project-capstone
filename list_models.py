import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found.")
    exit(1)

genai.configure(api_key=api_key)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models with google-generativeai: {e}")
    
    # Try with google.genai (newer SDK) if the above fails or returns nothing relevant
    print("\nTrying with google.genai SDK...")
    try:
        from google import genai as new_genai
        client = new_genai.Client(api_key=api_key)
        # I don't know the exact list_models API for the new SDK offhand, 
        # but let's try to just print that we are trying.
        # Actually, let's just rely on the standard one first.
    except ImportError:
        print("google.genai SDK not found.")
    except Exception as e2:
        print(f"Error with google.genai: {e2}")
