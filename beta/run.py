import os
import platform


if platform.system() == "Linux":
    os.system("urxvt -e bash -c './game'")
elif platform.system() == "Darwin":
    os.system(str(os.system("echo $TERM")) + "-e bash -c './game'")
elif platform.system() == "Windows":
    os.system("start cmd /k game")