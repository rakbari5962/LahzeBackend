def format_customer_experience(
    insights: dict
):
    """
    Convert internal customer insights data
    into frontend-ready customer experience format.
    """


    experiences = []


    attributes = insights.get(
        "attributes",
        []
    )


    for item in attributes:


        total_mentions = item.get(
            "total_mentions",
            0
        )


        positive_mentions = item.get(
            "positive_mentions",
            0
        )


        negative_mentions = item.get(
            "negative_mentions",
            0
        )


        positive_percentage = item.get(
            "positive_percentage",
            0
        )


        negative_percentage = item.get(
            "negative_percentage",
            0
        )



        # Confidence based on number of mentions

        if total_mentions >= 10:

            confidence = "high"

        elif total_mentions >= 5:

            confidence = "medium"

        else:

            confidence = "low"



        experiences.append({

            "title": item["label"],

            "total_mentions": total_mentions,

            "positive_mentions": positive_mentions,

            "negative_mentions": negative_mentions,

            "positive_percentage": positive_percentage,

            "negative_percentage": negative_percentage,

            "confidence": confidence

        })



    return {

        "title": "تجربه مشتریان",

        "items": experiences

    }