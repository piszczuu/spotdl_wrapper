cd /D "%~dp0"
if not exist .venv\ (
    py -m venv .venv
    pip install -r dependencies.txt
)
.venv\Scripts\activate.bat