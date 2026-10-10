from app.models.account import Account


def test_account_identity_unique_constraint_is_declared():
    matching = [
        constraint
        for constraint in Account.__table__.constraints
        if constraint.name == "uq_accounts_owner_type_owner_id_account_type"
    ]

    assert len(matching) == 1
    assert tuple(
        column.name for column in matching[0].columns
    ) == ("owner_type", "owner_id", "account_type")
