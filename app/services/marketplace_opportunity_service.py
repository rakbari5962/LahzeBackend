from datetime import datetime, timezone


from sqlalchemy.orm import Session


from app.models.opportunity import Opportunity

from app.models.business import Business

from app.models.service import Service

from app.services.business_visibility_service import (
    get_business_visibility_detail
)





def get_marketplace_opportunities(

    db: Session,

    city_id: int,

    category: str | None = None

):


    now = datetime.now(timezone.utc)



    query = (

        db.query(

            Opportunity,

            Business,

            Service

        )

        .join(

            Business,

            Opportunity.business_id == Business.id

        )

        .join(

            Service,

            Opportunity.service_id == Service.id

        )

        .filter(

            Opportunity.status == "ACTIVE",

            Opportunity.end_time > now,

            Business.city_id == city_id

        )

        .order_by(

            Opportunity.end_time.asc()

        )

    )



    results = query.all()



    opportunities = []



    for opportunity, business, service in results:



        visibility = get_business_visibility_detail(

            db=db,

            business_id=business.id

        )



        if not visibility["visible"]:

            continue



        if category:


            if not service.category:

                continue


            if service.category != category:

                continue



        remaining_seconds = (

            opportunity.end_time.astimezone(timezone.utc) - now

        ).total_seconds()



        remaining_minutes = max(

            0,

            int(

                remaining_seconds / 60

            )

        )



        opportunities.append(

            {

                "opportunity_id": opportunity.id,

                "business_id": business.id,

                "business_name": business.name,

                "service_id": service.id,

                "service_name": service.name,

                "city_id": business.city_id,

                "start_time": opportunity.start_time.isoformat(),

                "end_time": opportunity.end_time.isoformat(),

                "original_price": opportunity.original_price,

                "discount_percent": opportunity.discount_percent,

                "final_price": opportunity.final_price,

                "remaining_minutes": remaining_minutes

            }

        )



    return opportunities