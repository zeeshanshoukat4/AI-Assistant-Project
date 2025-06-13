import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
import time
import random

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Define all required classes
class Agent:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

class OpenAIChatCompletionsModel:
    def __init__(self, model, openai_client):
        self.model = model
        self.openai_client = openai_client

class RunConfig:
    def __init__(self, model, model_provider, tracing_disabled=True):
        self.model = model
        self.model_provider = model_provider
        self.tracing_disabled = tracing_disabled

class Runner:
    @staticmethod
    async def run(agent, input, run_config):
        client = run_config.model_provider
        response = client.chat.completions.create(
            model=run_config.model.model,
            messages=[
                {"role": "system", "content": agent.instructions},
                {"role": "user", "content": input}
            ]
        )
        
        class Result:
            def __init__(self, final_output):
                self.final_output = final_output
                
        return Result(final_output=response.choices[0].message.content)

# OpenAI client setup
client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# Agent definition
Materials_Engineering = Agent(
    name="Materials Engineering Agent",
    instructions="You are a Materials Engineering Agent. Provide in-depth info about any material with respect to metallurgy and materials engineering."
)

# Streamlit UI setup
st.set_page_config(page_title="🧪 Materials Expert", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f3f4f6;
    }
    .title {
        font-size: 3em;
        color: #2563eb;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .subtitle {
        font-size: 1.2em;
        color: #4b5563;
        text-align: center;
        margin-bottom: 2em;
    }
    .response-box {
        background-color: #e0f2fe;
        border-left: 6px solid #0284c7;
        padding: 1.2em;
        border-radius: 10px;
        font-size: 1.1em;
        color: #1e3a8a;
        white-space: pre-wrap;
    }
    .retry-info {
        color: #dc2626;
        font-size: 0.9em;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and subtitle
st.markdown('<div class="title">Materials Engineering Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">🔍 Enter a material name to get expert analysis</div>', unsafe_allow_html=True)

# Input
material_name_info = st.text_input("🧬 Material Name")

if st.button("Get Info"):
    if not material_name_info.strip():
        st.warning("⚠️ Please enter a valid material name.")
    else:
        with st.spinner("Fetching expert-level material info..."):
            async def run_agent_with_retry():
                max_retries = 5
                retry_delay = 1  # Initial delay in seconds
                
                for attempt in range(max_retries):
                    try:
                        return await Runner.run(
                            Materials_Engineering,
                            input=material_name_info,
                            run_config=config
                        )
                    except Exception as e:
                        if "503" in str(e) or "overloaded" in str(e):
                            st.warning(f"⚠️ Model overloaded. Retrying in {retry_delay:.1f}s... (attempt {attempt+1}/{max_retries})")
                            sleep_time = retry_delay + random.uniform(0, 1)
                            await asyncio.sleep(sleep_time)
                            retry_delay *= 2
                        else:
                            raise e
                
                raise Exception("Model is still overloaded after multiple retries. Please try again later.")

            try:
                result = asyncio.run(run_agent_with_retry())
                st.success("✅ Info Retrieved")
                st.markdown(f"### 📘 {material_name_info.capitalize()} Details:")
                st.markdown(f'<div class="response-box">{result.final_output}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                if "overloaded" in str(e):
                    st.info("💡 Tip: This error usually resolves quickly. Try again in 1-2 minutes.")