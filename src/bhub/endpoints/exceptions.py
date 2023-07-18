class BankDataAlreadyExistsException(Exception):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class BankDataNotFoundException(Exception):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class CustomerAlreadyExistsException(Exception):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class CustomerNotFoundException(Exception):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
