from sqlalchemy.orm import Session


from app.repositories.admin_reward_repository import (
    get_pending_rewards,
    get_processed_rewards,
    get_failed_release_transactions,
    get_reward_statistics
)



# --------------------------------------------------
# تبدیل RewardEvent به خروجی Admin
# --------------------------------------------------

def serialize_reward_event(
    reward_event
):

    return {

        "reward_event_id": reward_event.id,

        "user_id": reward_event.user_id,

        "booking_id": reward_event.booking_id,

        "amount": reward_event.amount,

        "type": reward_event.type,

        "status": reward_event.status,

        "transaction_id": reward_event.transaction_id,

        "created_at": reward_event.created_at

    }





# --------------------------------------------------
# Pending Rewards
# --------------------------------------------------

def get_pending_rewards_admin(
    db: Session
):

    rewards = get_pending_rewards(
        db
    )


    return {

        "count": len(rewards),

        "items": [

            serialize_reward_event(
                reward
            )

            for reward in rewards

        ]

    }





# --------------------------------------------------
# Processed Rewards
# --------------------------------------------------

def get_processed_rewards_admin(
    db: Session
):

    rewards = get_processed_rewards(
        db
    )


    total_amount = sum(
        reward.amount
        for reward in rewards
    )


    return {

        "count": len(rewards),

        "total_amount": total_amount,

        "items": [

            serialize_reward_event(
                reward
            )

            for reward in rewards

        ]

    }





# --------------------------------------------------
# Failed Release Transactions
# --------------------------------------------------

def serialize_failed_transaction(
    transaction
):

    return {

        "transaction_id": transaction.transaction_id,

        "type": transaction.type,

        "status": transaction.status,

        "amount": transaction.total_amount,

        "reference_type": transaction.reference_type,

        "reference_id": transaction.reference_id,

        "created_at": transaction.created_at

    }





def get_failed_rewards_admin(
    db: Session
):

    transactions = get_failed_release_transactions(
        db
    )


    return {

        "count": len(transactions),

        "items": [

            serialize_failed_transaction(
                transaction
            )

            for transaction in transactions

        ]

    }





# --------------------------------------------------
# Dashboard Statistics
# --------------------------------------------------

def get_reward_dashboard_stats(
    db: Session
):

    return get_reward_statistics(
        db
    )