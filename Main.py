import streamlit as st
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Runner
from dotenv import load_dotenv
import os


# STEP 1: Directly set your Gemini API key (for testing purpose only)
# Replace the string below with your actual Gemini API key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
# Gemini client setup
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
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

            async def run_agent():
                return await Runner.run(
                    Materials_Engineering,
                    input=material_name_info,
                    run_config=config
                )

            try:
                result = asyncio.run(run_agent())
                st.success("✅ Info Retrieved")
                st.markdown(f"### 📘 {material_name_info.capitalize()} Details:")
                st.markdown(f'<div class="response-box">{result.final_output}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")