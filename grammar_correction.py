import aiohttp
from config import AZURE_API_KEY, AZURE_ENDPOINT

async def correct_grammar_with_azure(text):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY
    }

    data = {
        "messages": [{"role": "user", "content": f"Please correct the grammatical structure such that it makes meaningful sense and don't add additional content, just send the output: {text}"}],
        "model": "gpt-o1"
    }

    async with aiohttp.ClientSession() as session:
        response = await session.post(AZURE_ENDPOINT, headers=headers, json=data)
        if response.status == 200:
            response_json = await response.json()
            corrected_text = response_json['choices'][0]['message']['content']
            return corrected_text
        else:
            return text
