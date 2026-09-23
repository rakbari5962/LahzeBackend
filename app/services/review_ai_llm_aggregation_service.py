from collections import defaultdict


MODEL_VERSION = "llm-aggregation-v1"



def aggregate_review_ai_results(
    review_results: list
):
    """
    Aggregate Gemini review analysis results
    into business-level review intelligence.
    """


    topic_stats = defaultdict(
        lambda: {
            "topic": "",
            "category": "",
            "label": "",
            "mentions": 0,
            "positive_mentions": 0,
            "negative_mentions": 0,
            "neutral_mentions": 0,
            "evidence": []
        }
    )



    for result in review_results:


        topics = result.get(
            "topics",
            []
        )


        for item in topics:


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



            evidence = item.get(
                "evidence"
            )


            if evidence:

                stats["evidence"].append(
                    evidence
                )



    strengths = []

    weaknesses = []



    for topic, stats in topic_stats.items():


        if (
            stats["positive_mentions"]
            >
            stats["negative_mentions"]
        ):

            strengths.append(
                stats
            )


        elif (
            stats["negative_mentions"]
            >
            stats["positive_mentions"]
        ):

            weaknesses.append(
                stats
            )



    return {

        "strengths": strengths,

        "weaknesses": weaknesses,

        "themes": list(
            topic_stats.values()
        ),

        "model_version": MODEL_VERSION

    }