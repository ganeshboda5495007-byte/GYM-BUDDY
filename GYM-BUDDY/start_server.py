import subprocess
import os

os.chdir(r"C:\Users\ganes\OneDrive\Desktop\New folder (4)\AI_Gym_Fitness")
subprocess.Popen(["python", "app.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
print("Server started!")
