from collections import defaultdict


MODEL_VERSION = "llm-aggregation-v2"



def unique_list(items):

    return list(
        dict.fromkeys(items)
    )



def aggregate_review_ai_results(
    review_results: list
):

    topic_stats = defaultdict(
        lambda: {
            "topic": "",
            "category": "",
            "label": "",
            "mentions": 0,
            "positive_mentions": 0,
            "negative_mentions": 0,
            "neutral_mentions": 0,
            "mixed_mentions": 0,
            "evidence": []
        }
    )



    for result in review_results:

        for item in result.get(
            "topics",
            []
        ):

            topic = item.get(
                "topic"
            )

            if not topic:
                continue



            stats = topic_stats[topic]

            stats["topic"] = topic

            stats["category"] = item.get(
                "category"
            )

            stats["label"] = item.get(
                "label"
            )

            stats["mentions"] += 1



            sentiment = item.get(
                "sentiment"
            )


            if sentiment == "positive":

                stats["positive_mentions"] += 1


            elif sentiment == "negative":

                stats["negative_mentions"] += 1


            elif sentiment == "neutral":

                stats["neutral_mentions"] += 1


            elif sentiment == "mixed":

                stats["mixed_mentions"] += 1



            evidence = item.get(
                "evidence"
            )


            if evidence:

                stats["evidence"].append(
                    evidence
                )



    strengths = []

    weaknesses = []

    themes = []



    for topic, stats in topic_stats.items():


        stats["evidence"] = unique_list(
            stats["evidence"]
        )


        themes.append(
            stats
        )



        positive = stats["positive_mentions"]

        negative = stats["negative_mentions"]

        mixed = stats["mixed_mentions"]



        # اگر حتی یک تجربه منفی یا mixed وجود دارد
        # دیگر strength خالص نیست

        if negative > 0 or mixed > 0:


            weaknesses.append(
                stats
            )


        elif positive > 0:


            strengths.append(
                stats
            )



    return {

        "strengths": strengths,

        "weaknesses": weaknesses,

        "themes": themes,

        "model_version": MODEL_VERSION

    }