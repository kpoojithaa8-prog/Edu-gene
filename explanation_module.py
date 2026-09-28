import os
from dotenv import load_dotenv

load_dotenv()

# Model identifier specified in documentation
MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"

explain_tokenizer = None
explain_model = None
_load_attempted = False


def load_explanation_model():
    """
    Load the LaMini-Flan-T5-783M model and tokenizer.
    Checks local Hugging Face cache first. If not cached, respects DOWNLOAD_LOCAL_MODEL setting
    to avoid unexpected ~3GB downloads during development or server boot.
    """
    global explain_tokenizer, explain_model, _load_attempted
    if _load_attempted:
        return explain_tokenizer, explain_model

    _load_attempted = True
    use_local = os.getenv("USE_LOCAL_MODEL", "true").lower() in ("true", "1", "yes")
    if not use_local:
        return None, None

    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        import torch

        # Check if already downloaded/cached locally
        try:
            explain_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)
            explain_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, local_files_only=True)
            print(f"Loaded cached local model '{MODEL_NAME}'.")
            return explain_tokenizer, explain_model
        except Exception:
            pass

        # If download is explicitly permitted in .env
        download_allowed = os.getenv("DOWNLOAD_LOCAL_MODEL", "false").lower() in ("true", "1", "yes")
        if download_allowed:
            print(f"Downloading local model '{MODEL_NAME}' (~3GB)...")
            explain_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            explain_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
            print(f"Successfully loaded '{MODEL_NAME}'.")
        else:
            print(
                f"Notice: Local model '{MODEL_NAME}' is not cached. Using Gemini fallback. "
                f"(Set DOWNLOAD_LOCAL_MODEL=true in .env to download local weights)"
            )
    except Exception as e:
        print(f"Notice: Local model '{MODEL_NAME}' unavailable: {e}. Using Gemini fallback.")

    return explain_tokenizer, explain_model


def explain_topic(topic: str) -> str:
    """
    Explains a concept in a simple and clear way for a school student.
    Uses local MBZUAI/LaMini-Flan-T5-783M if available, with automatic fallback
    to Gemini 1.5 Pro to ensure uninterrupted educational support.
    """
    tokenizer, model = load_explanation_model()

    if tokenizer is not None and model is not None:
        try:
            input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
            inputs = tokenizer(input_text, return_tensors="pt")

            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )

            explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return explanation
        except Exception as e:
            print(f"⚠️ Local generation error: {e}. Falling back to Gemini.")

    # Graceful fallback to Gemini 1.5 Pro
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            prompt = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
            try:
                gemini_model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
                response = gemini_model.generate_content(prompt)
                return response.text.strip()
            except Exception:
                gemini_model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                response = gemini_model.generate_content(prompt)
                return response.text.strip()
        else:
            return "⚠️ GEMINI_API_KEY is not set in .env and local model is not downloaded. Please add GEMINI_API_KEY to .env."
    except Exception as e:
        return f"⚠️ Error in Explanation: {e}"
