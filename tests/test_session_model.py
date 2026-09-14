from app.database.database import Base, engine

from app.models.session import Session





def test_session_model():


    print(
        "SESSION MODEL TEST"
    )

    print(
        "================="
    )


    Base.metadata.create_all(
        bind=engine
    )


    print()

    print(
        "TABLES:"
    )

    print(
        Base.metadata.tables.keys()
    )


    assert "sessions" in Base.metadata.tables


    print()

    print(
        "SESSION MODEL PASSED ✅"
    )





if __name__ == "__main__":

    test_session_model()