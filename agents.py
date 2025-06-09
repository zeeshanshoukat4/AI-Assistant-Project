
class AsyncOpenAI:
    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.openai.com/v1"

    async def chat(self, messages, model="gpt-3.5-turbo"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": messages
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/chat/completions", json=data, headers=headers) as resp:
                response_json = await resp.json()
                return response_json["choices"][0]["message"]["content"]


class OpenAIChatCompletionsModel:
    def __init__(self, model, openai_client):
        self.model = model
        self.client = openai_client


class RunConfig:
    def __init__(self, model, model_provider, tracing_disabled=True):
        self.model = model
        self.model_provider = model_provider
        self.tracing_disabled = tracing_disabled


class Agent:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions


class Runner:
    @staticmethod
    async def run(agent, input, run_config):
        messages = [
            {"role": "system", "content": agent.instructions},
            {"role": "user", "content": input}
        ]
        result = await run_config.model_provider.chat(messages, model=run_config.model.model)
        return type("Result", (), {"final_output": result})
