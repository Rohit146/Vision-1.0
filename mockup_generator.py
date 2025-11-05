from openai import OpenAI
import os
from dotenv import load_dotenv
import base64

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_text_mockup(user_prompt, data_summary, role="Business Analyst"):
    """
    Step 1: Generate a structured business mockup (text)
    """
    full_prompt = f"""
    You are a {role} AI assistant.
    Using the dataset summary and the user's request,
    create a clear, structured business mockup — such as a dashboard layout, report structure, or summary template.

    The mockup should include:
    - KPIs or metrics
    - Recommended visuals
    - Key insights
    - Logical section headers

    === Dataset Summary ===
    {data_summary}

    === User Request ===
    {user_prompt}

    Output in a clean, markdown-like format.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a senior business analyst AI who produces precise and professional drafts."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7,
    )
    text_result = response.choices[0].message.content.strip()
    return text_result


def generate_image_mockup(textual_mockup, role="Business Analyst"):
    """
    Step 2: Generate a relevant visual mockup using the textual structure as design context
    """
    image_prompt = f"""
    Design a professional business dashboard layout inspired by the following structured mockup:

    {textual_mockup}

    Requirements:
    - Use a modern dashboard design with KPIs, charts, and tables as described.
    - Use soft corporate colors and a clean layout.
    - Avoid text blocks; use chart placeholders and icons instead.
    - Style should match the tone of a {role} presentation.
    """

    response = client.images.generate(
        model="gpt-image-1",
        prompt=image_prompt,
        size="1024x1024",
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    return image_bytes
