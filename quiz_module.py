import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


def clean_json_block(text: str) -> str:
    # Remove Markdown ```json code fences
    cleaned = re.sub(r"```(?:json)?\s*([\s\S]*?)\s*```", r"\1", text).strip()
    return cleaned


def generate_quiz(text: str) -> list:
    try:
        current_api_key = os.getenv("GEMINI_API_KEY")
        if not current_api_key:
            return [{"error": "⚠️ GEMINI_API_KEY is not set. Please add your API key to the .env file."}]
        genai.configure(api_key=current_api_key)

        prompt = f"""
You are a quiz generator.

From the following passage, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON**, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage:
{text}
"""
        try:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
            response = model.generate_content(prompt)
        except Exception:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content(prompt)

        quiz_text = response.text.strip()

        # Clean markdown code blocks if any
        cleaned_text = clean_json_block(quiz_text)

        # Attempt to parse json directly
        try:
            quiz_data = json.loads(cleaned_text)
        except json.JSONDecodeError:
            # Fallback: extract substring between first '[' and last ']'
            match = re.search(r"(\[.*\])", cleaned_text, re.DOTALL)
            if match:
                quiz_data = json.loads(match.group(1))
            else:
                raise

        return quiz_data
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return [{"error": f"⚠️ Error in Quiz: {e}"}]
