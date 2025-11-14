from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handler para erros de validação do Pydantic"""
    logger.warning(f"Validation error on {request.url}: {len(exc.errors())} errors")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Dados inválidos",
            "errors": exc.errors()
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler para HTTPExceptions"""
    logger.warning(f"HTTP {exc.status_code} on {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handler para exceções gerais"""
    logger.error(f"Unexpected error on {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )