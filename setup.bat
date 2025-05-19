cd /D "%~dp0"
if not exist .venv\ (
    py -m venv .venv
)
.venv\Scripts\activate.bat