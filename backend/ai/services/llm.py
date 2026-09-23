from django.conf import settings


class LLMService:
    """Responsible for communicating with an LLM"""
    def __init__(self, client):
        self.client = client

    def generate_answer(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        if not response.choices:
            return []
        return response.choices[0].message.content