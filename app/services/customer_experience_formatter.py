def format_customer_experience(
    insights: dict
):
    """
    Convert internal customer insights data
    into frontend-ready customer experience format.
    """

    strengths = []

    improvements = []


    for item in insights.get("strengths", []):

        strengths.append({

            "title": item["label"],

            "status": "strength",

            "percentage": item["score"],

            "mentions": item["total_mentions"],

            "color": "green"

        })



    for item in insights.get("improvements", []):

        improvements.append({

            "title": item["label"],

            "status": "improvement",

            "percentage": item["score"],

            "mentions": item["total_mentions"],

            "color": "red"

        })


    return {

        "title": "تجربه مشتریان",

        "strengths": strengths,

        "improvements": improvements

    }