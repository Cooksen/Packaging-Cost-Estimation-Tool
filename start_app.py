import subprocess
import sys
import os

command = [
    "streamlit", "run", os.path.join("src", "cli", "run_app.py")
]

print("=" * 60)
print("Starting Packaging Cost Estimation Tool...")
print("A new browser window should open automatically.")
print("The server is now running.")
print("\nIMPORTANT:")
print("To stop the server, press Enter in THIS window.")
print("=" * 60)

try:
    server_process = subprocess.Popen(command, shell=True)
    
    input()

finally:
    print("\nStopping the server...")
    server_process.terminate() 
    print("Server has been stopped. You can close this window now.")
    import time
    time.sleep(2)