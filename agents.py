import os
from typing import Any, Dict, List, Optional
import asyncio
from abc import ABC, abstractmethod
from openai import AsyncOpenAI

class Agent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions

    async def run(self, input: str, run_config: 'RunConfig') -> 'Result':
        # Implement the logic to run the agent based on the input and configuration
        return await Runner.run(self, input, run_config)

class Result:
    def __init__(self, final_output: str):
        self.final_output = final_output

class RunConfig:
    def __init__(self, model: Any, model_provider: Any, tracing_disabled: bool):
        self.model = model
        self.model_provider = model_provider
        self.tracing_disabled = tracing_disabled

class Runner:
    @staticmethod
    async def run(agent: Agent, input: str, run_config: RunConfig) -> Result:
        # Implement the logic to run the agent with the given input and configuration
        messages = [
            {"role": "system", "content": agent.instructions},
            {"role": "user", "content": input}
        ]
        response = await run_config.model.create(messages)
        final_output = response["choices"][0]["message"]["content"]
        return Result(final_output)

class AsyncOpenAI:
    def __init__(self, api_key: str, base_url: str):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def chat_completions_create(self, model: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response

class OpenAIChatCompletionsModel:
    def __init__(self, model: str, openai_client: AsyncOpenAI):
        self.model = model
        self.openai_client = openai_client

    async def create(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        return await self.openai_client.chat_completions_create(self.model, messages)