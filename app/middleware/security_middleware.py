"""
Middleware de segurança para aplicar headers e validações
"""
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.security_config import SecurityConfig
import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware para aplicar configurações de segurança"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            # Processar request
            response = await call_next(request)
            
            # Aplicar headers de segurança
            for header, value in SecurityConfig.SECURITY_HEADERS.items():
                response.headers[header] = value
            
            # Remover headers que podem vazar informações
            response.headers.pop("server", None)
            response.headers.pop("x-powered-by", None)
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erro no middleware de segurança: {str(e)}")
            try:
                # Em caso de erro, continuar sem os headers
                response = await call_next(request)
                return response
            except Exception as inner_e:
                logger.critical(f"Erro crítico no middleware: {str(inner_e)}")
                raise HTTPException(status_code=500, detail="Erro interno do servidor")