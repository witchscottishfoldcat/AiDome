from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional

class AppException(Exception):
    """Base application exception."""
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code

class UserNotFoundException(AppException):
    """Raised when a user is not found."""
    def __init__(self, user_id: int):
        super().__init__(f"User with id {user_id} not found", 404)

def register_exception_handlers(app: FastAPI):
    """Register exception handlers for the application."""
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.code,
            content={"message": exc.message},
        )