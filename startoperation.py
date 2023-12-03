import os

print(os.getcwd())
# basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)
# os.chdir(basedir)
print(os.getcwd())
os.system(".venv\Scripts\activate")
os.system("start chrome http://localhost:5000 ")
os.system("python.exe app/main.py")
input()
#  c:/Users/clinic/Desktop/abdElhameed_project/System/.venv/Scripts/python.exe c:/Users/clinic/Desktop/abdElhameed_project/System/app/main.py
