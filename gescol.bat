@echo off
REM Definição para o caminho do executável
set PROJECT_DIR=C:\Users\_figur\Documents\GesCol_Gestor_EQ_LOG\Python\GesCol

REM Define o caminho para o script de ativação do ambiente virtual
set VENV_ACTIVATE=%PROJECT_DIR%\.venv\Scripts\activate.bat

REM Define o caminho para o seu arquivo principal da aplicação (assumindo que seja 'app.py' na raiz do projeto)
set MAIN_APP=%PROJECT_DIR%\app.py

REM Ativa o ambiente virtual
call %VENV_ACTIVATE%

REM Navega até o diretório do projeto
cd /d %PROJECT_DIR%

REM Executa o arquivo principal da aplicação Python
python %MAIN_APP%

REM Desativa o ambiente virtual (opcional)
deactivate
pause