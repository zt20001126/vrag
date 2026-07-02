import requests

from app.core.config import settings


def _is_configured(value: str | None) -> bool:
    return bool(value and value.strip() and not value.startswith("your_"))


class LlmService:
    def generate_prompt(self, text: str) -> dict[str, object]:
        return self._chat(
            system_prompt="You are a visual design prompt assistant.",
            user_prompt=f"Generate an image generation prompt from this design requirement: {text}",
        )

    def optimize_prompt(self, prompt: str) -> dict[str, object]:
        return self._chat(
            system_prompt="You optimize prompts for image generation while preserving user intent.",
            user_prompt=f"Optimize this prompt for high-quality visual generation: {prompt}",
        )

    def _chat(self, system_prompt: str, user_prompt: str) -> dict[str, object]:
        if not _is_configured(settings.DEEPSEEK_API_KEY):
            return {
                "provider": "deepseek",
                "configured": False,
                "message": "DEEPSEEK_API_KEY is not configured.",
            }

        try:
            response = requests.post(
                settings.DEEPSEEK_API_URL,
                headers={
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.DEEPSEEK_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.7,
                },
                timeout=settings.REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            return {
                "provider": "deepseek",
                "configured": True,
                "success": False,
                "message": f"DeepSeek request failed: {exc}",
            }

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content")
        )
        return {
            "provider": "deepseek",
            "configured": True,
            "model": settings.DEEPSEEK_MODEL,
            "content": content,
            "raw": data,
        }


llm_service = LlmService()
