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

st.set_page_config(page_title="Brand Identity Generator", page_icon="🎨")
st.title("🌈 Brand Identity Generator")
st.write("Powered by OpenRouter and Mistral 7B")

idea = st.text_input("💡 What does your startup do?")
audience = st.text_input("🎯 Who is your target audience?")
tone = st.selectbox("🎭 Choose your brand's tone", ["Professional", "Playful", "Luxury", "Minimal", "Bold"])

if st.button("🚀 Generate Brand Identity"):
    if not idea.strip():
        st.warning("Please enter your startup idea.")
    else:
        with st.spinner("Thinking... Generating brand identity..."):
            prompt = build_prompt(idea, audience, tone)
            try:
                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                st.subheader("🧾 Brand Identity")
                st.text(result.strip())

                hex_codes = re.findall(r"#[0-9a-fA-F]{6}", result)
                if hex_codes:
                    st.subheader("🎨 Color Palette")
                    for code in hex_codes:
                        st.markdown(
                            f"<div style='display:inline-block;width:100px;height:40px;background-color:{code};border-radius:5px;margin:4px'></div> <span>{code}</span>",
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No color codes found in the output.")

            except Exception as e:
                st.error(f"API Error: {e}")
                st.info("Tip: Check your API key and model access on OpenRouter.ai")