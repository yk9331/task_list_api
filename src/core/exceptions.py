from typing import Any, Dict, Optional

from fastapi import HTTPException, status

import src.core.error_msg as error_msg


class BaseException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=message, headers=headers)


class ClientError(BaseException):
    def __init__(
        self,
        message: str = error_msg.CLIENT_ERROR_DEFAULT,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            headers=headers,
        )


class UnauthorizedError(BaseException):
    def __init__(
        self,
        message: str = error_msg.UNAUTHORIZED_DEFAULT,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            headers=headers,
        )


class ForbiddenError(BaseException):
    def __init__(
        self,
        message: str = error_msg.FORBIDDEN_DEFAULT,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            headers=headers,
        )


class NotFoundError(BaseException):
    def __init__(
        self,
        message: str = error_msg.NOT_FOUND_DEFAULT,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            headers=headers,
        )


class ConflictError(BaseException):
    def __init__(
        self,
        message: str = error_msg.CONFLICT_DEFAULT,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            headers=headers,
        )


class InteralServerError(BaseException):
    def __init__(
        self,
        message: str = error_msg.INTERNAL_SERVER_ERROR_DEFAULT,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            headers=headers,
        )
