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


def analyze_review_with_gemini(
    review_text: str,
    rating: int | None = None
):

    prompt = f"""
You are an AI customer-review analyst for a marketplace platform.

Your job is to understand the meaning of a customer review
and extract structured information from it.

Analyze the review semantically.

Do NOT rely only on keywords.

A single review may contain multiple topics.

For each meaningful topic:

1. Identify the topic.
2. Determine the sentiment toward that topic.
3. Determine the intensity of the sentiment.
4. Extract only the relevant evidence from the review.
5. Explain briefly why the evidence supports the classification.

Important:

- Do not invent information.
- Do not infer facts that are not present.
- Do not treat unrelated parts of the review as evidence.
- A review can contain both positive and negative feedback.
- Different topics in the same review must be analyzed independently.
- If the customer says something positive and then gives a limitation,
  preserve the nuance.
- "گران ولی ارزشمند" is NOT simply negative.
- "خوب بود ولی انتظار زیاد بود" contains separate positive and negative topics.
- Evidence must be a short exact or near-exact phrase from the review.
- Do not rewrite evidence into a new claim.
- Ignore irrelevant information.
- Use professional and neutral classification.

Allowed sentiment values:

positive
negative
neutral
mixed

Allowed intensity values:

low
medium
high

Possible topics include, but are NOT limited to:

quality
staff_behavior
price
waiting_time
cleanliness
equipment
communication
location
booking
support
delivery
value
accuracy
availability

Use a new topic when the review clearly discusses something
that does not fit the examples above.

Review:

{review_text}

Rating:

{rating}

Return ONLY valid JSON.

Return exactly this structure:

{{
    "topics": [
        {{
            "topic": "",
            "label": "",
            "sentiment": "",
            "intensity": "",
            "evidence": "",
            "reason": ""
        }}
    ]
}}
"""


    models = [
        MODEL_NAME,
        FALLBACK_MODEL
    ]


    for model in models:

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            text = response.text.strip()


            text = text.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()


            result = json.loads(text)


            if not isinstance(result, dict):
                raise ValueError(
                    "Gemini response is not an object"
                )


            if "topics" not in result:
                raise ValueError(
                    "Gemini response does not contain topics"
                )


            if not isinstance(
                result["topics"],
                list
            ):
                raise ValueError(
                    "topics must be a list"
                )


            return result


        except Exception as e:

            print(
                "GEMINI REVIEW ANALYSIS ERROR:",
                model,
                e
            )


    raise Exception(
        "Gemini review analysis unavailable"
    )