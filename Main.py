import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Load API key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize OpenAI Client
client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=10.0
)

# Materials Expert Agent
class MaterialsExpert:
    def __init__(self):
        self.instructions = (
           "You are a highly qualified expert in Materials and Metallurgical Engineering."  
"Provide structured, concise, and technically accurate responses."  
"Focus on the following key aspects for each material:"  

"1. Composition: Include elemental or chemical makeup and highlight relevant phases or microstructures. "  
"2. Mechanical & Physical Properties: Cover properties such as hardness, tensile strength, ductility, impact resistance, thermal/electrical conductivity, and corrosion behavior."  
"3. Industrial Applications: Specify sectors and use-cases (e.g., automotive, aerospace, biomedical, construction, energy)."  
"4. Manufacturing Methods : Describe typical forming, casting, joining, heat treatment, or surface engineering processes used for the material."  
"5. Recent Innovations : Mention notable advancements such as alloy developments, coatings, additive manufacturing, or nanomaterials."  
"6. Historical Relevance : Briefly explain the material's historical significance or evolution in industrial use."  

"Ensure the response does not exceed 800 words (every heading 133 words).cover all and completed respone in 900 words ok with all headings and data"  
"Use professional, academically appropriate language that is clear and accessible to both engineers and students."  
"Avoid redundancy and overly complex terminology without explanation."

    
        )

    def get_info(self, material_name):
        try:
            response = client.chat.completions.create(
                model="gemini-2.0-flash",
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": f"Provide technical details about {material_name}"}
                ],
                temperature=0.3,
                max_tokens=1000  # Increased to allow full response
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

# Streamlit UI setup
st.set_page_config(page_title="🧪 Materials Engineering Assistant", layout="centered")

# Optional CSS styling (titles only)
st.markdown("""
    <style>
    .title {
        font-size: 3em;
        font-weight: bold;
        color: #0f172a;
        text-align: center;
        margin-bottom: 0.3em;
        font-family: 'Segoe UI', sans-serif;
    }
    .subtitle {
        text-align: center;
        color: #475569;
        margin-bottom: 1em;
        font-size: 1.1em;
    }
    .loading {
        display: inline-block;
        width: 24px;
        height: 24px;
        border: 4px solid rgba(0,0,0,.2);
        border-top-color: #3b82f6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

# UI Title
st.markdown('<div class="title">🧪 Materials Engineering Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter any material name for expert-level metallurgical insights</div>', unsafe_allow_html=True)

# Input
material_name = st.text_input("🔍 Enter Material Name", key="material_input")

# Button + Logic
if st.button("Analyze Material", key="analyze_btn"):
    if not material_name.strip():
        st.warning("⚠️ Please enter a material name.")
    else:
        with st.spinner("Thinking like a metallurgist..."):
            expert = MaterialsExpert()
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
                st.success(f"✅ Analysis complete in {(end_time - start_time):.1f} seconds")
                # ✅ Use st.write() to allow full rendering of tables and long text
                st.write(response)
                st.caption("💡 Tip: For more detailed insights, include material grade or intended usage (e.g., 316L Stainless Steel for implants).")
