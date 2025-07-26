cd ..
python -m venv .venv
.venv\Scripts\pip.exe install torch==2.7.1 --index-url https://download.pytorch.org/whl/cu126
.venv\Scripts\pip.exe install -r requirements.txt
.venv\Scripts\pip.exe install -r requirements-dev.txt
pause
