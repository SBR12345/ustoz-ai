"""Groq API client for Ustoz.AI using the OpenAI-compatible SDK."""

from openai import OpenAI


BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "llama-3.3-70b-versatile"


def _system_message(output_lang: str) -> str:
    if output_lang == "uz":
        return (
            "Siz O'zbekiston o'qituvchilari uchun yordamchisiz. "
            "Javobni faqat o'zbek tilida va lotin yozuvida yozing. "
            "Rus tilidagi sarlavha, izoh yoki jumlalardan foydalanmang."
        )
    if output_lang == "en":
        return (
            "You are an assistant for teachers in Uzbekistan. "
            "Write the entire response in English only. "
            "Do not use Russian or Uzbek headings, notes, or sentences."
        )
    return (
        "Вы — помощник учителей Узбекистана. "
        "Отвечайте только на русском языке."
    )


def generate_material(api_key: str, prompt: str, output_lang: str) -> str:
    client = OpenAI(api_key=api_key, base_url=BASE_URL)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": _system_message(output_lang)},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def run_quality_check(api_key: str, prompt: str, output_lang: str) -> str:
    client = OpenAI(api_key=api_key, base_url=BASE_URL)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": _system_message(output_lang)},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
