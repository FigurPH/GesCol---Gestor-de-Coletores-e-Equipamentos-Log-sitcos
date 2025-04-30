import logging
import functools
import time
from typing import Callable, Any

# Configuração global do logger
logging.basicConfig(
    filename="log_gescol.log",  # Salva os logs no arquivo log_gescol.log
    filemode="a",              # Modo de escrita (append)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG         # Nível de log padrão
)

class LogExecution:
    def __init__(
        self,
        level: int = logging.DEBUG,
        log_args: bool = True,
        log_result: bool = False,
        log_time: bool = True,
        log_exception: bool = True,
        logger: logging.Logger = None
    ):
        """
        Inicializa o decorador com as configurações de logging.

        Args:
            level: Nível de log (ex: logging.INFO, logging.DEBUG).
            log_args: Se True, loga os argumentos da função.
            log_result: Se True, loga o valor de retorno.
            log_time: Se True, loga o tempo de execução.
            log_exception: Se True, loga exceções (nível ERROR).
            logger: Instância do logger a ser usada. Padrão é o logger do módulo.
        """
        self.level = level
        self.log_args = log_args
        self.log_result = log_result
        self.log_time = log_time
        self.log_exception = log_exception
        self.logger = logger or logging.getLogger(__name__)

    def __call__(self, func: Callable) -> Callable:
        """
        Torna a classe utilizável como um decorador.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                if self.log_args:
                    self.logger.log(self.level, f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
                
                result = func(*args, **kwargs)

                if self.log_result:
                    self.logger.log(self.level, f"{func.__name__} returned {result}")
                
                if self.log_time:
                    elapsed_time = time.time() - start_time
                    self.logger.log(self.level, f"{func.__name__} executed in {elapsed_time:.4f} seconds")
                
                return result
            except Exception as e:
                if self.log_exception:
                    self.logger.error(f"Exception in {func.__name__}: {e}", exc_info=True)
                raise
        return wrapper