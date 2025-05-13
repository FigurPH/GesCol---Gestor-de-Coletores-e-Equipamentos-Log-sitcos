import logging

# Configuração global do logger

_logger = logging.basicConfig(
    filename="log_gescol.log",  # Salva os logs no arquivo log_gescol.log
    filemode="a",                # Modo de escrita (append)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO         # Nível de log padrão
)

def logger(func, log_level: int = 2):
    def wrapper(*args, **kwargs):
        match log_level:
            case 1:
                _logger.log(func.__name__)
            case 2:...
            case 3:...
            case 4:...
            case 5:...