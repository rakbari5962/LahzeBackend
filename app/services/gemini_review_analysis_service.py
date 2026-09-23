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



ALLOWED_TOPICS = {

    "quality": {
        "category": "service_quality",
        "label": "کیفیت خدمات"
    },

    "staff_behavior": {
        "category": "customer_experience",
        "label": "برخورد پرسنل"
    },

    "price": {
        "category": "pricing",
        "label": "قیمت"
    },

    "value": {
        "category": "price_perception",
        "label": "ارزش نسبت به قیمت"
    },

    "waiting_time": {
        "category": "operations",
        "label": "زمان انتظار"
    },

    "cleanliness": {
        "category": "environment",
        "label": "نظافت و محیط"
    },

    "equipment": {
        "category": "facilities",
        "label": "تجهیزات و امکانات"
    },

    "communication": {
        "category": "customer_experience",
        "label": "ارتباط با مشتری"
    },

    "support": {
        "category": "customer_support",
        "label": "پشتیبانی"
    },

    "delivery": {
        "category": "fulfillment",
        "label": "تحویل"
    },

    "booking": {
        "category": "booking_experience",
        "label": "رزرو"
    },

    "trust": {
        "category": "trust",
        "label": "اعتماد"
    }

}



def validate_topics(data):

    valid_topics = []


    for item in data.get("topics", []):


        topic = item.get("topic")


        if topic not in ALLOWED_TOPICS:

            continue



        topic_info = ALLOWED_TOPICS[topic]


        item["category"] = topic_info["category"]

        item["label"] = topic_info["label"]



        if item.get("sentiment") not in [
            "positive",
            "negative",
            "neutral",
            "mixed"
        ]:

            continue



        if item.get("intensity") not in [
            "low",
            "medium",
            "high"
        ]:

            continue



        if not item.get("evidence"):

            continue



        valid_topics.append(item)



    return {

        "topics": valid_topics

    }





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
- Preserve nuance.
- Evidence must be copied from the review.
- Do not rewrite evidence.
- Ignore irrelevant information.

Allowed sentiment values:

positive
negative
neutral
mixed


Allowed intensity values:

low
medium
high


Possible topics:

quality
staff_behavior
price
waiting_time
cleanliness
equipment
communication
support
delivery
value
booking
trust


Category rules:

Category must represent the broader meaning of the topic.

Examples:

quality -> service_quality
staff_behavior -> customer_experience
price -> pricing
value -> price_perception
waiting_time -> operations
cleanliness -> environment
equipment -> facilities
communication -> customer_experience
support -> customer_support
delivery -> fulfillment
booking -> booking_experience
trust -> trust


Create a new topic only if it is clearly important
and cannot fit existing topics.


Review:

{review_text}


Rating:

{rating}


Return ONLY valid JSON.

Return exactly this JSON format:

{{
    "topics": [
        {{
            "topic": "",
            "category": "",
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


            return validate_topics(result)



        except Exception as e:

            print(
                "GEMINI REVIEW ANALYSIS ERROR:",
                model,
                e
            )



    raise Exception(
        "Gemini review analysis unavailable"
    )