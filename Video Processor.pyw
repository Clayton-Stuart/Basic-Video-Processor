import os
import subprocess

# set working directory to file
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.system(".\\env\\Scripts\\activate")
subprocess.Popen(".\\env\\Scripts\\pythonw.exe .\\lib\\main.pyw")
os.system("exit")