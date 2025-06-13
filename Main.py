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
    timeout=15.0  # Increased timeout for detailed responses
)

# Enhanced Agent class for comprehensive responses
class MaterialsExpert:
    def __init__(self):
        self.instructions = """
        You are a Senior Materials Engineering Professor with 30 years of experience. 
        Provide extremely detailed, technical information about any material covering ALL aspects:
        
        1. BASIC INFORMATION:
        - Chemical composition (exact percentages)
        - Crystal structure
        - Phase diagram analysis
        - Microstructure characteristics
        
        2. MECHANICAL PROPERTIES:
        - Tensile strength (with values at different temperatures)
        - Yield strength
        - Hardness (multiple scales)
        - Fatigue resistance
        - Fracture toughness
        - Creep behavior
        
        3. PHYSICAL PROPERTIES:
        - Density
        - Melting point
        - Thermal conductivity
        - Electrical conductivity
        - Thermal expansion coefficient
        - Magnetic properties
        
        4. MANUFACTURING & PROCESSING:
        - Common production methods
        - Forming techniques
        - Heat treatment procedures
        - Machinability rating
        - Weldability analysis
        - Surface treatment options
        
        5. APPLICATIONS:
        - Industry uses (with specific examples)
        - Component examples
        - Advantages for specific applications
        - Limitations in service
        
        6. ENVIRONMENTAL FACTORS:
        - Corrosion resistance
        - Oxidation behavior
        - Radiation resistance
        - Chemical compatibility
        - Recycling potential
        
        7. RECENT ADVANCEMENTS:
        - New research findings
        - Emerging applications
        - Alternative materials
        - Future development trends
        
        Provide data tables when appropriate.
        Include relevant equations where applicable.
        Mention standard specifications (ASTM, ISO, etc.).
        Minimum 800 words response required.
        """

    def get_info(self, material_name):
        try:
            response = client.chat.completions.create(
                model="gemini-1.5-pro",  # Using more capable model
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": f"Provide exhaustive technical details about {material_name}"}
                ],
                temperature=0.2,  # More factual
                max_tokens=3000,   # Longer response
                top_p=0.9
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

# Streamlit UI setup
st.set_page_config(page_title="🧪 Advanced Materials Expert", layout="wide")

# Enhanced CSS for better readability
st.markdown("""
    <style>
    .title {
        font-size: 2.8em;
        color: #2563eb;
        text-align: center;
        margin-bottom: 0.3em;
        font-weight: 700;
    }
    .response-box {
        background-color: #f8fafc;
        border-left: 5px solid #0369a1;
        padding: 1.5em;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        line-height: 1.7;
        font-size: 1.05em;
    }
    .section-header {
        color: #075985;
        font-weight: 600;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        font-size: 1.3em;
        border-bottom: 2px solid #bae6fd;
        padding-bottom: 0.3em;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 1em 0;
    }
    th, td {
        border: 1px solid #cbd5e1;
        padding: 8px 12px;
        text-align: left;
    }
    th {
        background-color: #e0f2fe;
    }
    .loading {
        display: inline-block;
        width: 24px;
        height: 24px;
        border: 4px solid rgba(0,0,0,.1);
        border-radius: 50%;
        border-top-color: #0369a1;
        animation: spin 1s linear infinite;
        margin-right: 10px;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

# UI Components
st.markdown('<div class="title">Advanced Materials Analysis System</div>', unsafe_allow_html=True)
st.caption("""<div style='text-align:center;margin-bottom:2em'>Get exhaustive technical analysis of any engineering material</div>""", 
           unsafe_allow_html=True)

col1, col2 = st.columns([0.7, 0.3])
with col1:
    material_name = st.text_input("**🧬 Enter Material Name/Alloy/Compound**", 
                                placeholder="e.g., Titanium Grade 5, Inconel 718, Carbon Fiber Composite")
    
    detail_level = st.select_slider(
        "**Detail Level**",
        options=["Basic", "Standard", "Technical", "Comprehensive", "Research-Level"],
        value="Comprehensive"
    )

with col2:
    st.markdown("""
    <div style='background-color:#f0f9ff;padding:1em;border-radius:8px;border-left:4px solid #0369a1'>
    <h4 style='color:#075985;margin-top:0'>Tips:</h4>
    <ul style='padding-left:1.2em'>
    <li>Use specific names (e.g., "316L Stainless Steel")</li>
    <li>Include alloy designations when known</li>
    <li>For composites, specify matrix/reinforcement</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

if st.button("**Generate Comprehensive Analysis**", type="primary", use_container_width=True):
    if not material_name.strip():
        st.warning("Please enter a material name")
    else:
        with st.spinner(""):
            expert = MaterialsExpert()
            
            loading_placeholder = st.empty()
            loading_html = """
            <div style='text-align:center;margin:2em 0'>
                <span class="loading"></span>
                <span style='font-size:1.1em;color:#0369a1'>
                    Compiling exhaustive technical dossier for {}...
                </span>
            </div>
            """.format(material_name)
            loading_placeholder.markdown(loading_html, unsafe_allow_html=True)
            
            start_time = time.time()
            response = expert.get_info(f"{material_name} ({detail_level} analysis requested)")
            end_time = time.time()
            
            loading_placeholder.empty()
            
            if response.startswith("Error:"):
                st.error(response)
            else:
                st.success(f"Analysis generated in {(end_time-start_time):.1f} seconds")
                st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
                
                # Add download button
                st.download_button(
                    label="Download Full Analysis",
                    data=response,
                    file_name=f"{material_name.replace(' ', '_')}_technical_analysis.txt",
                    mime="text/plain"
                )