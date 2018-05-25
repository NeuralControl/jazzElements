import os
import subprocess

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

with cd("d:\\Code\\jazzElements\\jazzElements"):
   subprocess.call("python -m cProfile -o base.prof base.py")
   subprocess.call("snakeviz.exe base.prof")



