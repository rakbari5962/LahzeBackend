import json
from pathlib import Path

from app.database.database import SessionLocal

from app.models.review_attribute import ReviewAttribute



JSON_FILE = Path(
    "business_attributes_master_v1_final.json"
)



def seed_business_attributes():

    db = SessionLocal()

    inserted = 0
    skipped = 0


    try:

        with open(
            JSON_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            attributes = json.load(file)



        for item in attributes:


            exists = (
                db.query(ReviewAttribute)
                .filter(
                    ReviewAttribute.key == item["key"]
                )
                .first()
            )


            if exists:

                skipped += 1

                continue



            attribute = ReviewAttribute(

                key=item["key"],

                label=item["label"],

                category=item.get("category")

            )


            db.add(attribute)

            inserted += 1



        db.commit()



        print("Seed completed")

        print(
            f"Inserted: {inserted}"
        )

        print(
            f"Skipped: {skipped}"
        )



    except Exception as e:

        db.rollback()

        print(
            "Seed failed:",
            e
        )


    finally:

        db.close()



if __name__ == "__main__":

    seed_business_attributes()