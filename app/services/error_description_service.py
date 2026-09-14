from sqlalchemy.orm import Session


from app.models.error_occurrence import ErrorOccurrence

from app.models.error_definition import ErrorDefinition





def generate_error_description(
    db: Session,
    occurrence_id: int
):


    occurrence = db.query(
        ErrorOccurrence
    ).filter(

        ErrorOccurrence.id == occurrence_id

    ).first()



    if not occurrence:

        return None





    definition = db.query(
        ErrorDefinition
    ).filter(

        ErrorDefinition.error_code == occurrence.error_code

    ).first()




    context = occurrence.context or {}



    title = "خطای ناشناخته"



    if definition:

        title = definition.name





    description = f"""
عنوان خطا:
{title}


کد خطا:
{occurrence.error_code}


عملیات:
{occurrence.action}


شرح سیستم:
{definition.description if definition else 'اطلاعات تعریف خطا موجود نیست.'}


جزئیات فنی:
"""




    for key, value in context.items():

        description += (
            f"\n{key}: {value}"
        )




    return description.strip()