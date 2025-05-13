import google.generativeai as genai
import os 

API_KEY = "AIzaSyArUDVwxItsfr9lp4a10gh4sQOTRTsknXE"  #Generated API Key

if not API_KEY or API_KEY == "AIzaSyCUyp6pdify_swdJr03CWGZ9PJJnfriiNk":
    print("Error with your API id!!")
    exit()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Prompt
prompt = "Tell me a short story about kerala."

# API call
try:
    print("Sending prompt to Gemini API: ",prompt)
    response = model.generate_content(prompt)

    # Print Output
    print("\nGemini API Response :\n")
    print(response.text)

except Exception as e:
    print("\nAn error occurred: ",e)