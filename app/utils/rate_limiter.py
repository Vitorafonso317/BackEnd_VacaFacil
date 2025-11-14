from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from typing import Dict
import time

class RateLimiter:
    def __init__(self, max_keys: int = 10000):
        self.requests: Dict[str, list] = {}
        self.max_keys = max_keys
        self.last_cleanup = datetime.now()
    
    def is_allowed(self, key: str, max_requests: int = 100, window_minutes: int = 1) -> bool:
        try:
            now = datetime.now()
            window_start = now - timedelta(minutes=window_minutes)
            
            # Limpeza periódica para evitar vazamento de memória
            if (now - self.last_cleanup).total_seconds() > 300:  # 5 minutos
                self._cleanup_old_entries(now)
                self.last_cleanup = now
            
            if key not in self.requests:
                self.requests[key] = []
            
            # Limpar requests antigos
            self.requests[key] = [req_time for req_time in self.requests[key] if req_time > window_start]
            
            # Verificar limite
            if len(self.requests[key]) >= max_requests:
                return False
            
            # Adicionar request atual
            self.requests[key].append(now)
            return True
        except Exception:
            # Em caso de erro, permitir a requisição
            return True
    
    def _cleanup_old_entries(self, now: datetime):
        """Remove entradas antigas para evitar vazamento de memória"""
        try:
            cutoff = now - timedelta(hours=1)
            keys_to_remove = []
            
            for key, requests in self.requests.items():
                # Remove requests muito antigos
                self.requests[key] = [req for req in requests if req > cutoff]
                # Se não há requests recentes, remove a chave
                if not self.requests[key]:
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del self.requests[key]
            
            # Se ainda há muitas chaves, remove as mais antigas
            if len(self.requests) > self.max_keys:
                sorted_keys = sorted(self.requests.keys(), 
                                   key=lambda k: max(self.requests[k]) if self.requests[k] else datetime.min)
                keys_to_remove = sorted_keys[:len(self.requests) - self.max_keys]
                for key in keys_to_remove:
                    del self.requests[key]
        except Exception as e:
            # Log do erro e limpar tudo em caso de falha crítica
            import logging
            logging.error(f"Rate limiter cleanup error: {str(e)}")
            self.requests.clear()

rate_limiter = RateLimiter()

def check_rate_limit(request: Request, max_requests: int = 100):
    try:
        client_ip = request.client.host if request.client else "unknown"
        if not rate_limiter.is_allowed(client_ip, max_requests):
            raise HTTPException(
                status_code=429,
                detail="Muitas requisições. Tente novamente em alguns minutos."
            )
    except HTTPException:
        raise
    except Exception as e:
        # Log do erro mas permitir requisição
        import logging
        logging.warning(f"Rate limiter error: {str(e)}")
        pass