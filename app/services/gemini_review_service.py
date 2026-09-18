import time
import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODEL_NAME = "models/gemini-flash-latest"

FALLBACK_MODEL = "models/gemini-flash-lite-latest"



def generate_business_summary_with_gemini(
    business_analysis: dict
):

    prompt = f"""
You are an AI reputation manager for a marketplace platform.

Your task is to write a professional Persian business profile summary based on customer feedback analysis.

Rules:

- You are writing an AI reputation analysis for a business profile.
- Do not write a promotional advertisement.
- Help customers understand the real customer experience.
- Identify the most important strengths and weaknesses.
- Explain why each strength or weakness matters for customer experience.
- Do not simply list topics.
- Prioritize the most meaningful feedback.
- Avoid vague statements.
- Mention improvements in a constructive and polite way.

IMPORTANT OUTPUT RULES:

- The "summary" field must start with:
"بر اساس بازخوردهای ثبت‌شده،"

- Never mention:
  - ratings
  - percentages
  - review counts
  - numerical statistics

- Do not use exaggerated marketing words like:
  "بهترین"
  "بی‌نظیر"
  "فوق‌العاده‌ترین"

- Write in professional Persian.
- Output ONLY valid JSON.

Input analysis:

{json.dumps(
    business_analysis,
    ensure_ascii=False,
    indent=2
)}


Return exactly this JSON format:

{{
    "summary": "",
    "positive_summary": "",
    "improvement_summary": ""
}}
"""


    models = [
        MODEL_NAME,
        FALLBACK_MODEL
    ]


    response = None


    for model in models:

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            break


        except Exception as e:

            print(
                "GEMINI ERROR:",
                model,
                e
            )

            time.sleep(10)



    if not response:

        raise Exception(
            "Gemini models unavailable"
        )



    text = response.text.strip()


    text = text.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    ).strip()



    try:

        return json.loads(text)


    except json.JSONDecodeError:

        return {

            "summary": text,

            "positive_summary": None,

            "improvement_summary": None

        }