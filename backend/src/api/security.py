"""
JWT verification dependency per ADR-001 in plan.md

Per @specs/002-phase2-webapp/plan.md#adr-001
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from src.config import Settings


class SecurityError(HTTPException):
    """Custom exception for security errors"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
) -> int:
    """
    FastAPI dependency that extracts and validates JWT token

    Per ADR-001: JWT Verification Strategy in FastAPI
    - Extracts JWT from Authorization header
    - Validates token signature and expiration
    - Raises 401 for invalid/missing tokens
    - Returns user_id for route handlers
    """

    if credentials is None:
        raise SecurityError(detail="Authentication required")

    try:
        # Verify token signature
        settings = Settings()
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=["HS256"]
        )

        # Verify user_id claim exists
        user_id: int = payload.get("sub")
        if user_id is None:
            raise SecurityError(detail="Invalid token: missing user claim")

        return user_id

    except ExpiredSignatureError:
        raise SecurityError(detail="Token has expired")
    except JWTError:
        raise SecurityError(detail="Invalid token")
    except Exception as e:
        # Log unexpected errors but return generic message
        raise SecurityError(detail="Authentication failed")


async def get_current_user(
    user_id: Annotated[int, Depends(get_current_user_id)]
) -> int:
    """
    Convenience dependency that returns user_id directly

    This is the primary dependency used in protected routes
    """
    return user_id
