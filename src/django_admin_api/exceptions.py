class AdminApiError(Exception):
    """Base exception for Admin API."""


class AlreadyRegisteredError(AdminApiError):
    def __init__(self, model: type[object]) -> None:
        super().__init__(
            f"Model {model.__module__}.{model.__name__} is already registered"
        )

        self.model = model


class NotRegisteredError(AdminApiError):
    def __init__(self, model: type[object]) -> None:
        super().__init__(
            f"Model {model.__module__}.{model.__name__} is not registered"
        )
