import os
import platform
import sys
import time

# Static Variables
try:
    screen_width = os.get_terminal_size().columns
except:
    screen_width = 90
    pass


# Static Functions
def clear():
    if platform.system() in ["Linux", "Darwin"]:
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
    else:
        raise ValueError("No known operating system.")


def speech_manipulation(text, speed):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)


def confirmation():
    input("Press ENTER to continue.")


def title(name: str):
    clear()
    print("#" * screen_width)
    print("#" + " " * int((screen_width - len(name)) / 2 - 1) + name + " " * int(
        (screen_width - len(name)) / 2 - 1) + "#")
    print("#" * screen_width + "\n")


def game_over():
    clear()
    speech_manipulation("Ouh there you are again.\n", 0.05)
    speech_manipulation(
        "Don't get me wrong. This is no surprise for me. Maybe you have more luck in your next reincarnation.\n",
        0.05)
    speech_manipulation("Have a good day. :)", 0.07)
    time.sleep(2)
    sys.exit()
