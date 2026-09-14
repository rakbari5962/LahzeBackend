from app.database.database import (
    engine,
    Base
)


# Register Error Models
from app.models.error_definition import ErrorDefinition
from app.models.error_occurrence import ErrorOccurrence
from app.models.error_report import ErrorReport



def create_tables():

    print("REGISTERED TABLES:")
    print("==================")

    print(
        Base.metadata.tables.keys()
    )


    print()
    print("CREATING ERROR TABLES")
    print("====================")


    Base.metadata.create_all(
        bind=engine
    )


    print(
        "ERROR TABLES CREATED"
    )



if __name__ == "__main__":

    create_tables()