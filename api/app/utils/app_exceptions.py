from fastapi import Request
from starlette.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )


class AppException:
    class _AppExceptionTemplate(AppExceptionCase):
        def __init__(self, status_code: int, description: str, context: dict = None):
            self.description = description
            super().__init__(status_code, context)

    class UserNotFound(_AppExceptionTemplate):
        def __init__(self, context: dict = None):
            super().__init__(404, "User not found", context)

    class UsernameAlreadyExists(_AppExceptionTemplate):
        def __init__(self, context: dict = None):
            super().__init__(400, "Username already exists", context)

    class CreateUser(_AppExceptionTemplate):
        def __init__(self, context: dict = None):
            super().__init__(500, "User creation failed", context)

    class UserNotModified(_AppExceptionTemplate):
        def __init__(self, context: dict = None):
            super().__init__(304, "User not modified", context)

    class JumpNotFound(_AppExceptionTemplate):
        def __init__(self, context: dict = None):
            super().__init__(404, "Jump not found", context)

    class CreateJump(_AppExceptionTemplate):
        def __init__(self, context: dict = None):
            super().__init__(500, "Jump creation failed", context)

    class JumpNotModified(_AppExceptionTemplate):
        def __init__(self, context: dict = None):
            super().__init__(304, "Jump not modified", context)

    class LandingNotFound(_AppExceptionTemplate):
        def __init__(self, context: dict = None):
            super().__init__(404, "Landing not found", context)         
