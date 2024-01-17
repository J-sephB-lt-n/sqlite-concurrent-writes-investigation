import os
import subprocess

for filename in os.listdir("."):
    if filename[:11] == "database.db":
        subprocess.run(["rm", filename])
