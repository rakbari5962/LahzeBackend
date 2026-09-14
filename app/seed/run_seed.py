from app.database.database import SessionLocal

from app.seed.business_category_seed import (
    seed_business_categories
)



def run():

    db = SessionLocal()

    try:

        seed_business_categories(db)

        print(
            "Business categories seeded successfully"
        )

    finally:

        db.close()



if __name__ == "__main__":

    run()