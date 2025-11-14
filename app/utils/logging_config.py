import logging
import sys
from datetime import datetime

def setup_logging():
    """Configurar logging da aplicação"""
    
    # Criar formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Handler para arquivo (com tratamento de erro)
    try:
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.ERROR)
    except Exception:
        file_handler = None  # Se não conseguir criar arquivo, usar apenas console
    
    # Configurar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    
    if file_handler:
        root_logger.addHandler(file_handler)
    else:
        logging.warning("Não foi possível criar arquivo de log, usando apenas console")
    
    # Logger específico da aplicação
    app_logger = logging.getLogger("vacafacil")
    app_logger.setLevel(logging.INFO)
    
    return app_logger