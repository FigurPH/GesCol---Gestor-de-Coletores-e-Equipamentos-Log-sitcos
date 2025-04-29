# --- Configuração do Path ---
$ProjectDir = $PSScriptRoot

# Caminho para o pythonw.exe do venv
$PythonWExe = Join-Path $ProjectDir ".venv\Scripts\pythonw.exe"

# Caminho para o app.py
$MainApp = Join-Path $ProjectDir "app.py"

# Executa GesCol
Start-Process -FilePath $PythonWExe -ArgumentList $MainApp -WorkingDirectory $ProjectDir -WindowStyle Hidden