import os
import streamlit as st

from groq import Groq
from dotenv import load_dotenv


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Content",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# 2. LOAD API KEY
# ==========================================

load_dotenv()

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    API_KEY = os.getenv("GROQ_API_KEY")


# ==========================================
# 3. INITIALIZE GROQ CLIENT
# ==========================================

if API_KEY:
    client = Groq(api_key=API_KEY)
else:
    client = None


# ==========================================
# 4. GROQ RESPONSE FUNCTION
# ==========================================

def generate_response(prompt):

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7
    )

    return response.choices[0].message.content


# ==========================================
# 5. WEBSITE HEADER
# ==========================================

st.title("🤖 AI Content Generator")

st.write(
    "Generate Instagram content, captions "
    "and hashtags using AI."
)

st.divider()


# ==========================================
# 6. USER INPUT
# ==========================================

st.subheader("Enter Your Details")

topic = st.text_input(
    "Enter Your Topic",
    placeholder="Example: Artificial Intelligence"
)

audience = st.text_input(
    "Target Audience",
    placeholder="Example: College Students"
)


# ==========================================
# 7. GENERATE CONTENT BUTTON
# ==========================================

if st.button("Generate AI Content"):

    if not API_KEY:

        st.error("Groq API Key is missing.")

    elif not topic.strip() or not audience.strip():

        st.warning("Please enter both topic and audience.")

    else:

        try:

            with st.spinner("Generating AI Content..."):

                # PROMPT 1

                prompt1 = f"""
                Create simple Instagram content about {topic}.

                Target audience: {audience}.
                """

                content = generate_response(prompt1)


                # PROMPT 2

                prompt2 = f"""
                Based on the following content,
                create an attractive Instagram caption.

                Content:
                {content}
                """

                caption = generate_response(prompt2)


                # PROMPT 3

                prompt3 = f"""
                Generate 5 relevant Instagram hashtags
                based on this caption:

                {caption}
                """

                hashtags = generate_response(prompt3)


            # ==================================
            # 8. DISPLAY FINAL OUTPUT
            # ==================================

            st.success("Content Generated Successfully!")

            st.divider()

            st.subheader("📝 Generated Content")

            st.write(content)

            st.divider()

            st.subheader("📢 Instagram Caption")

            st.write(caption)

            st.divider()

            st.subheader("#️⃣ Generated Hashtags")

            st.write(hashtags)


        except Exception as e:

            st.error(f"Something went wrong: {e}")


# ==========================================
# 9. FOOTER
# ==========================================

st.divider()

st.caption("Built using Python + Groq SDK + Streamlit")