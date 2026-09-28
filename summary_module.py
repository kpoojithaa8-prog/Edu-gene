import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


def summarize_text(text: str) -> str:
    try:
        current_api_key = os.getenv("GEMINI_API_KEY")
        if not current_api_key:
            return "⚠️ GEMINI_API_KEY is not set. Please add your API key to the .env file."
        genai.configure(api_key=current_api_key)

        prompt = f"Summarize the following text in simple language:\n\n{text}"
        try:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
            response = model.generate_content(prompt)
        except Exception:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content(prompt)

        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error in Summary: {e}"
