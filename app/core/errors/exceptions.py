from app.core.errors.error_codes import ErrorCodes



class LahzeException(Exception):

    def __init__(
        self,
        error_code: int,
        message: str,
        context: dict = None
    ):

        self.error_code = error_code

        self.message = message

        self.context = context or {}

        super().__init__(message)




class BookingException(LahzeException):

    pass




class SettlementException(LahzeException):

    pass




class WalletException(LahzeException):

    pass




class PaymentException(LahzeException):

    pass