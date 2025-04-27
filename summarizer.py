import requests
import os
import time

API_URL = "https://api-inference.huggingface.co/models/google/pegasus-xsum"

API_TOKEN = "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"


headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def summarize_text(text, retries=3):
    payload = {
    "inputs": (
        "Summarize the following medical case in 3 sentences, including the patient's symptoms, diagnosis, treatment, and outcome. Avoid repeating phrases:\n\n"
        + text
    ),
    "parameters": {
        "max_length": 300,
        "min_length": 50,
        "do_sample": False
    }
}


    for attempt in range(retries):
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            try:
                result = response.json()
                if isinstance(result, list) and "summary_text" in result[0]:
                    return result[0]["summary_text"]
                return f"⚠️ Unexpected format: {result}"
            except Exception as e:
                return f"❌ JSON decode error: {e}"

        elif response.status_code == 503:
            print("⏳ Model is warming up... retrying in 8 seconds.")
            time.sleep(8)
        else:
            return f"❌ API Error {response.status_code}: {response.text[:200]}"

    return "❌ API Error: Model did not respond after multiple attempts, please try again later."
