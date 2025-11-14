"""
Configurações de segurança da aplicação
"""
import secrets
import string
from typing import List

class SecurityConfig:
    """Configurações de segurança"""
    
    # Configurações de senha
    MIN_PASSWORD_LENGTH = 8
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_NUMBERS = True
    REQUIRE_SPECIAL_CHARS = False
    
    # Rate limiting
    DEFAULT_RATE_LIMIT = 100  # requests per minute
    AUTH_RATE_LIMIT = 10      # login attempts per minute
    
    # Headers de segurança
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

def generate_secure_key(length: int = 32) -> str:
    """Gerar chave segura aleatória"""
    try:
        if length < 16:
            raise ValueError("Comprimento mínimo da chave é 16 caracteres")
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    except Exception as e:
        import logging
        logging.error(f"Key generation error: {str(e)}")
        raise ValueError(f"Erro ao gerar chave: {str(e)}")

def validate_password(password: str) -> tuple[bool, List[str]]:
    """Validar força da senha"""
    errors = []
    
    if not password:
        errors.append("Senha não pode estar vazia")
        return False, errors
    
    if len(password) < SecurityConfig.MIN_PASSWORD_LENGTH:
        errors.append(f"Senha deve ter pelo menos {SecurityConfig.MIN_PASSWORD_LENGTH} caracteres")
    
    if SecurityConfig.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
        errors.append("Senha deve conter pelo menos uma letra maiúscula")
    
    if SecurityConfig.REQUIRE_LOWERCASE and not any(c.islower() for c in password):
        errors.append("Senha deve conter pelo menos uma letra minúscula")
    
    if SecurityConfig.REQUIRE_NUMBERS and not any(c.isdigit() for c in password):
        errors.append("Senha deve conter pelo menos um número")
    
    if SecurityConfig.REQUIRE_SPECIAL_CHARS and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        errors.append("Senha deve conter pelo menos um caractere especial")
    
    return len(errors) == 0, errors

def sanitize_input(text: str) -> str:
    """Sanitizar entrada do usuário"""
    if not text:
        return ""
    
    try:
        # Remover caracteres perigosos
        dangerous_chars = ["<", ">", "&", "\"", "'", "/", "\\"]
        sanitized = text
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")
        
        return sanitized.strip()
    except Exception as e:
        import logging
        logging.warning(f"Input sanitization error: {str(e)}")
        return ""  # Em caso de erro, retornar string vazia