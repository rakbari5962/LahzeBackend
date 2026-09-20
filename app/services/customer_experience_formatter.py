def format_customer_experience(
    insights: dict
):
    """
    Convert internal customer insights data
    into frontend-ready customer experience format.
    """

    experiences = []


    all_items = (
        insights.get("strengths", [])
        +
        insights.get("improvements", [])
    )


    for item in all_items:


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



        # Backward compatibility
        # until database contains sentiment split

        if (
            positive_mentions == 0
            and negative_mentions == 0
        ):

            if item in insights.get("strengths", []):

                positive_mentions = total_mentions

            else:

                negative_mentions = total_mentions



        total = (
            positive_mentions
            +
            negative_mentions
        )



        positive_percentage = (

            round(
                (
                    positive_mentions
                    /
                    total
                )
                * 100
            )

            if total > 0

            else 0

        )



        negative_percentage = (

            round(
                (
                    negative_mentions
                    /
                    total
                )
                * 100
            )

            if total > 0

            else 0

        )



        # Confidence based on number of customer mentions

        if total >= 10:

            confidence = "high"

        elif total >= 5:

            confidence = "medium"

        else:

            confidence = "low"



        experiences.append({

            "title": item["label"],

            "total_mentions": total,

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