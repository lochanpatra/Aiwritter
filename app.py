import streamlit as st
import requests

st.set_page_config(page_title="AI Writer with OpenRouter", page_icon="📝")
st.title("📝 AI Writer with OpenRouter")

prompt = st.text_area("Enter your writing prompt:", height=200)
model = "mistralai/mistral-7b-instruct:free"

API_KEY = st.secrets["OPENROUTER_API_KEY"]

if st.button("✍️ Generate Text"):
    if not prompt.strip():
        st.warning("Please enter a prompt before generating.")
    else:
        with st.spinner("Generating..."):
            res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 512,
                    "temperature": 0.7
                }
            )
        if res.status_code == 200:
            text = res.json()["choices"][0]["message"]["content"]
            st.success("Here's what the AI wrote:")
            st.write(text)
            st.download_button("📥 Download text", text, "ai.txt", "text/plain")
        else:
            st.error(f"Error {res.status_code}: {res.json().get('error', {}).get('message', '')}")
