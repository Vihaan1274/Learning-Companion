import requests
import json
from config import Config

def generate_answer(query, context_chunks, mode="explain", depth="beginner"):
    context_text = "\n".join(context_chunks)

    system_prompt = f"""You are a friendly AI learning companion.
    - Adjust explanations for {depth} level learners.
    - Be clear, encouraging, and use examples.
    - Modes: explain, quiz, analogy.
    """

    if mode == "quiz":
        user_prompt = f"Create 3-5 quiz questions about {query}.\nContext:\n{context_text}"
    elif mode == "analogy":
        user_prompt = f"Explain {query} using a simple analogy.\nContext:\n{context_text}"
    else:
        user_prompt = f"Explain {query} step by step.\nContext:\n{context_text}"

    payload = {
        "model": Config.OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5,
    }

    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": Config.SITE_URL,
        "X-Title": Config.SITE_TITLE,
    }

    response = requests.post(Config.OPENROUTER_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    else:
        return f"❌ Error {response.status_code}: {response.text}"
