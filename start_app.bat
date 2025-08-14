@echo off
echo Starting Packaging Cost Estimation Tool...
echo Please wait, a new browser window will open automatically.

:: Temporarily add Python and Poetry to the PATH for this session
set "PATH=%PATH%;C:\Program Files\Python311;%USERPROFILE%\AppData\Roaming\Python\Python311\Scripts"

:: Change to the project directory
cd "C:\Users\Sen_Chao\OneDrive - Dell Technologies\Desktop\project\cost_estimation"

poetry run python start_app.py
pause