from app.database.database import engine

from sqlalchemy import text



print("ADDING USER ROLE COLUMN")
print("======================")



with engine.connect() as conn:

    conn.execute(
        text(
            """
            ALTER TABLE users
            ADD COLUMN IF NOT EXISTS role VARCHAR
            DEFAULT 'CUSTOMER'
            NOT NULL;
            """
        )
    )

    conn.commit()



print("USER ROLE COLUMN CREATED")