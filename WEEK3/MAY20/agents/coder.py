from openai import AsyncOpenAI
from typing import Any

class Coder:
    def __init__(self):
        self.client = AsyncOpenAI(base_url="https://generativelanguage.googleapis.com/v1beta", api_key="AIzaSyCMK2D0I_qW4gVrlQd45tQ6cv1OOR7Mp90")

    async def respond(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="models/gemini-1.5-flash",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
