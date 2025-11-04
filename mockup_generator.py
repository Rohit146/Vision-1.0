from openai import OpenAI
import os
from dotenv import load_dotenv
import base64

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_text_mockup(user_prompt, data_summary, role="Business Analyst"):
    """Generate a structured business mockup (text)"""
    full_prompt = f"""
    You are a {role} AI assistant.
    Based on the dataset summary and the user's request, 
    draft a structured business mockup, report, or dashboard suggestion.

    === Dataset Summary ===
    {data_summary}

    === User Request ===
    {user_prompt}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional business analyst AI who produces clean, insightful business mockups."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def generate_image_mockup(user_prompt):
    """Generate a relevant image mockup using OpenAI Image API"""
    image_prompt = (
        f"Professional business dashboard or report layout for: {user_prompt}. "
        f"Minimalistic, clean UI, corporate color palette, with charts and KPIs."
    )

    response = client.images.generate(
        model="gpt-4.1-mini",
        prompt=image_prompt,
        size="1024x1024",
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    return image_bytes

