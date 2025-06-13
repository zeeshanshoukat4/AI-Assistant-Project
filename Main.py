import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize OpenAI client with timeout settings
client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=10.0  # Set timeout to 10 seconds
)

# Simplified Agent class
class MaterialsExpert:
    def __init__(self):
        self.instructions = """
        You are a Materials Engineering expert. Provide concise, technical information about 
        materials with respect to metallurgy and materials engineering. Focus on:
        - Composition
        - Mechanical properties
        - Common applications
        - Manufacturing considerations
        - Recent advancements
        Keep responses under 300 words.
        """

    def get_info(self, material_name):
        try:
            response = client.chat.completions.create(
                model="gemini-2.0-flash",
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": f"Provide technical details about {material_name}"}
                ],
                temperature=0.3,  # Less creative but more factual
                max_tokens=500   # Limit response length
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

# Streamlit UI setup
st.set_page_config(page_title="🧪 Materials Expert", layout="centered")

# Optimized CSS with loading animations
st.markdown("""
    <style>
    .title {
        font-size: 2.5em;
        color: #2563eb;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .response-box {
        background-color: #e0f2fe;
        border-left: 4px solid #0284c7;
        padding: 1em;
        border-radius: 8px;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0,0,0,.3);
        border-radius: 50%;
        border-top-color: #2563eb;
        animation: spin 1s ease-in-out infinite;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

# UI Components
st.markdown('<div class="title">Materials Engineering Assistant</div>', unsafe_allow_html=True)

material_name = st.text_input("🧬 Enter Material Name", key="material_input")

if st.button("Get Technical Analysis", key="analyze_btn"):
    if not material_name.strip():
        st.warning("Please enter a material name")
    else:
        with st.spinner(""):
            expert = MaterialsExpert()
            
            # Create a placeholder for dynamic loading
            loading_placeholder = st.empty()
            loading_placeholder.markdown(
                '<div style="text-align:center"><span class="loading"></span> Analyzing material properties...</div>',
                unsafe_allow_html=True
            )
            
            start_time = time.time()
            response = expert.get_info(material_name)
            end_time = time.time()
            
            loading_placeholder.empty()
            
            if response.startswith("Error:"):
                st.error(response)
            else:
                st.success(f"Analysis complete ({(end_time-start_time):.1f}s)")
                st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
                st.caption("💡 Tip: For more detailed analysis, try being more specific about the material grade or application.")