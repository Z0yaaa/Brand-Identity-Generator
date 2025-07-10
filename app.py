import streamlit as st
import openai
import re
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), 
    base_url="https://openrouter.ai/api/v1"
)

def build_prompt(idea, audience, tone):
    return f"""
You are a professional brand strategist.

Generate a brand identity for a startup.

Startup Description: {idea}
Target Audience: {audience}
Brand Tone: {tone}

Please return your answer in this exact format:

Brand Name: <Brand Name>
Tagline: <Tagline>
Personality: <Short personality description>
Color Palette:
- <hex code 1>
- <hex code 2>
- <hex code 3>
"""

st.set_page_config(page_title="Brand Identity Generator", page_icon="🎨", layout="centered")

st.markdown(
    """
    <style>
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: #4F8BF9;
        margin-bottom: 0.5em;
    }
    .subtext {
        color: #888;
        font-size: 1em;
        margin-top: -10px;
    }
    .color-box {
        display: inline-block;
        width: 80px;
        height: 40px;
        border-radius: 8px;
        margin: 6px 10px 6px 0;
        border: 1px solid #ccc;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>🌈 Brand Identity Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Powered by OpenRouter & Mistral 7B</div>", unsafe_allow_html=True)

st.markdown("---")

with st.container():
    st.markdown("### 💼 Startup Info")
    idea = st.text_input("💡 What does your startup do?", placeholder="Describe your idea")
    audience = st.text_input("🎯 Who is your target audience?", placeholder="E.g. Students, Travelers, Developers")
    tone = st.selectbox("🎭 Choose your brand's tone", ["Professional", "Playful", "Luxury", "Minimal", "Bold"])

st.markdown("---")

if st.button("🚀 Generate Brand Identity"):
    if not idea.strip():
        st.warning("⚠️ Please enter your startup idea to continue.")
    else:
        with st.spinner("✨ Generating your brand identity..."):
            prompt = build_prompt(idea, audience, tone)
            try:
                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content.strip()
                
                st.markdown("### 🧾 Generated Brand Identity")
                st.code(result, language="markdown")

                hex_codes = re.findall(r"#[0-9a-fA-F]{6}", result)
                if hex_codes:
                    st.markdown("### 🎨 Suggested Color Palette")
                    cols = st.columns(len(hex_codes))
                    for i, code in enumerate(hex_codes):
                        with cols[i]:
                            st.markdown(f"<div class='color-box' style='background-color:{code}'></div>", unsafe_allow_html=True)
                            st.caption(code)
                else:
                    st.info("🎨 No color hex codes were found in the response.")

            except Exception as e:
                st.error(f"❌ API Error: {e}")
                st.info("🔑 Tip: Check your API key and model access on [OpenRouter.ai](https://openrouter.ai)")
