import time
import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("JARVIS_API_KEY"),
    base_url=os.getenv("JARVIS_BASE_URL"),
    timeout=120
)


MODEL_NAME = os.getenv(
    "JARVIS_MODEL",
    "GROK_4_7"
)

FALLBACK_MODEL = "GROK_4_6"



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


        if topic:
            topic = (
                topic
                .strip()
                .lower()
                .replace("-", "_")
                .replace(" ", "_")
            )

            item["topic"] = topic



        sentiment = item.get("sentiment")

        if sentiment:
            item["sentiment"] = sentiment.lower()



        intensity = item.get("intensity")

        if intensity:
            item["intensity"] = intensity.lower()



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

            item["evidence"] = ""


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
4. Extract evidence.

Evidence is mandatory for every topic.

Rules:
- Evidence must be an exact quote copied from the review text.
- Do not summarize or rewrite the evidence.
- The evidence should directly support the topic and sentiment.
- Never return an empty evidence field.
- If a topic has no clear evidence in the review, do not include that topic.
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


Example:

Review:
"کیفیت خدمات عالی بود، برخورد پرسنل خوب بود ولی زمان انتظار کمی زیاد بود."

Expected topics:

{{
 "topics": [
   {{
     "topic": "quality",
     "sentiment": "positive",
     "intensity": "high",
     "evidence": "کیفیت خدمات عالی بود"
   }},
   {{
     "topic": "staff_behavior",
     "sentiment": "positive",
     "intensity": "medium",
     "evidence": "برخورد پرسنل خوب بود"
   }},
   {{
     "topic": "waiting_time",
     "sentiment": "negative",
     "intensity": "medium",
     "evidence": "زمان انتظار کمی زیاد بود"
   }}
 ]
}}



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


Important:
- Always use lowercase topic keys exactly as provided above.
- Do not create new topic keys.
- Do not return variations, translations, or capitalized versions.

Incorrect examples:

Quality
Staff_behavior
Waiting Time
service_quality

Correct examples:

quality
staff_behavior
waiting_time


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


Return ONLY a JSON object.
Do not return an array.
Do not return markdown.

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

            print(
                "CALLING MODEL:",
                model,
                "TEXT:",
                review_text[:80]
            )

            response = client.chat.completions.create(
                model=model,
                response_format={
                    "type": "json_object"
                },
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )


            text = response.choices[0].message.content.strip()

            print("RAW GROK:")
            print(text)


            text = text.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()



            try:
                result = json.loads(text)

            except Exception:
                print("RAW GEMINI RESPONSE:")
                print(text)
                raise


            if not isinstance(result, dict):

                print("RAW GEMINI RESPONSE:")
                print(text)

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