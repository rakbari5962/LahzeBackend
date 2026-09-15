from sqlalchemy.orm import Session

from app.repositories.account_repository import create_account



def create_user_wallet_account(
    db: Session,
    user_id: int
):

    return create_account(
        db,
        owner_type="USER",
        owner_id=user_id,
        account_type="CUSTOMER_WALLET"
    )





def create_business_revenue_account(
    db: Session,
    business_id: int
):

    return create_account(
        db,
        owner_type="BUSINESS",
        owner_id=business_id,
        account_type="BUSINESS_REVENUE"
    )





def create_platform_treasury_account(
    db: Session
):

    return create_account(
        db,
        owner_type="PLATFORM",
        owner_id=1,
        account_type="PLATFORM_TREASURY"
    )





def create_reward_payable_account(
    db: Session
):

    return create_account(
        db,
        owner_type="PLATFORM",
        owner_id=1,
        account_type="REWARD_PAYABLE"
    )


def create_commission_payable_account(
    db: Session
):

    return create_account(
        db,
        owner_type="PLATFORM",
        owner_id=1,
        account_type="COMMISSION_PAYABLE"
    )


def create_escrow_account(
    db: Session
):

    return create_account(
        db,
        owner_type="PLATFORM",
        owner_id=1,
        account_type="ESCROW"
    )





def initialize_platform_accounts(
    db: Session
):

    accounts = []


    # حساب کسب‌وکار نمونه
    # مثال: آترین
    business_account = create_business_revenue_account(
        db,
        business_id=1
    )

    accounts.append(
        business_account
    )


    # خزانه پلتفرم
    treasury_account = create_platform_treasury_account(
        db
    )

    accounts.append(
        treasury_account
    )


    # حساب بدهی Reward
    reward_account = create_reward_payable_account(
        db
    )

    accounts.append(
        reward_account
    )
    


    # حساب بدهی Commission
    commission_account = create_commission_payable_account(
        db
    )

    accounts.append(
        commission_account
    )

    # حساب واسط نگهداری پول رزروها
    escrow_account = create_escrow_account(
        db
    )

    accounts.append(
        escrow_account
    )


    return accounts